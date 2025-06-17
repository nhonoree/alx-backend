import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

function getItemById(id) {
  return listProducts.find((item) => item.itemId === id);
}

const client = createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

async function reserveStockById(itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock, 10) : 0;
}

const app = express();
const port = 1245;

app.get('/list_products', (_, res) => res.json(listProducts));

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) return res.json({ status: 'Product not found' });
  const reserved = await getCurrentReservedStockById(itemId);
  res.json({ ...item, currentQuantity: item.initialAvailableQuantity - reserved });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) return res.json({ status: 'Product not found' });
  const reserved = await getCurrentReservedStockById(itemId);
  const available = item.initialAvailableQuantity - reserved;
  if (available < 1) return res.json({ status: 'Not enough stock available', itemId });
  await reserveStockById(itemId, reserved + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

app.listen(port, () => console.log(`API available on localhost port ${port}`));
