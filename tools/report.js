const _ = require('lodash');

function renderReport(userTemplate, data) {
  return _.template(userTemplate)(data);
}

module.exports = { renderReport };

if (require.main === module) {
  console.log(renderReport(process.argv[2] || 'Report for <%= name %>', { name: 'demo' }));
}
