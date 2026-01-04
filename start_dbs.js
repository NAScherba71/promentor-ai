const { MongoMemoryServer } = require('mongodb-memory-server');
const { RedisMemoryServer } = require('redis-memory-server');

async function startServers() {
  const mongod = await MongoMemoryServer.create({
    instance: {
      port: 27017,
      ip: '127.0.0.1'
    }
  });
  console.log('MongoDB started at:', mongod.getUri());

  const redisServer = new RedisMemoryServer({
    instance: {
      port: 6379,
      ip: '127.0.0.1'
    }
  });
  await redisServer.start();
  console.log('Redis started on port 6379');

  // Keep process alive
  setInterval(() => {}, 1000);
}

startServers().catch(err => console.error(err));