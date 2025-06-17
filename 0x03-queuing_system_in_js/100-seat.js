import express from 'express';
import kue from 'kue';
import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();
const queue = kue.createQueue();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

let reservationEnabled = true;
const reserveSeat = async (number) => await setAsync('available_seats', number);
const getCurrentAvailableSeats = async () => parseInt(await getAsync('available_seats'), 10);

const app = express();
const port = 1245;

reserveSeat(50);

app.get('/available_seats', async (_, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) return res.json({ status: 'Reservation are blocked' });
  const job = queue.create('reserve_seat').save((err) => {
    if (err) return res.json({ status: 'Reservation failed' });
    res.json({ status: 'Reservation in process' });
  });
  job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
  job.on('failed', (err) => console.log(`Seat reservation job ${job.id} failed: ${err.message}`));
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    let available = await getCurrentAvailableSeats();
    if (available > 0) {
      await reserveSeat(available - 1);
      if (available - 1 === 0) reservationEnabled = false;
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});

app.listen(port, () => console.log(`Server running on port ${port}`));
