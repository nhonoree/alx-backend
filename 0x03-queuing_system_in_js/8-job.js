const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  for (const jobInfo of jobs) {
    const job = queue.create('push_notification_code_3', jobInfo).save((err) => {
      if (!err) console.log(`Notification job created: ${job.id}`);
    });

    job.on('complete', () => console.log(`Notification job ${job.id} completed`));
    job.on('failed', (err) => console.log(`Notification job ${job.id} failed: ${err.message}`));
    job.on('progress', (progress) => console.log(`Notification job ${job.id} ${progress}% complete`));
  }
};

export default createPushNotificationsJobs;
