const request = require('supertest');
const app = require('../app');

describe('API Health and Auth Endpoints', () => {
  it('GET /api/health returns 200 and running message', async () => {
    const res = await request(app).get('/api/health');
    expect(res.statusCode).toEqual(200);
    expect(res.body).toHaveProperty('success', true);
    expect(res.body.message).toContain('Server is running');
  });

  it('POST /api/auth/login rejects empty requests with 400', async () => {
    const res = await request(app).post('/api/auth/login').send({});
    expect(res.statusCode).toBeGreaterThanOrEqual(400);
  });

  it('GET /api/transactions requires authentication', async () => {
    const res = await request(app).get('/api/transactions');
    expect(res.statusCode).toEqual(401);
  });

  it('GET /api/budgets requires authentication', async () => {
    const res = await request(app).get('/api/budgets');
    expect(res.statusCode).toEqual(401);
  });

  it('GET /api/goals requires authentication', async () => {
    const res = await request(app).get('/api/goals');
    expect(res.statusCode).toEqual(401);
  });

  it('GET /api/admin/stats requires authentication', async () => {
    const res = await request(app).get('/api/admin/stats');
    expect(res.statusCode).toEqual(401);
  });

  it('GET /api/admin/users requires authentication', async () => {
    const res = await request(app).get('/api/admin/users');
    expect(res.statusCode).toEqual(401);
  });
});
