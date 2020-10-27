var run = require('tape')
var text = require('../')

run('it works', function(test) {
  var span = document.createElement('span')
  var value = 'npm.im/text-content'

  test.notOk(text(span), 'has no value')
  text(span, value)
  test.equal(text(span), value, 'set value found')
  test.end()
})

run('it clears', function(test) {
  var span = document.createElement('span')

  text(span, 'hi')
  test.equal(text(span), 'hi', 'value found')
  text(span, null)
  test.notOk(text(span), 'has no value')
  test.end()
})
