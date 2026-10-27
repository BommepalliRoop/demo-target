const test = require('node:test');
const assert = require('node:assert');
const { renderReport } = require('./report');

test('renders a template with data', () => {
  assert.strictEqual(renderReport('Hi <%= name %>', { name: 'Ada' }), 'Hi Ada');
});
