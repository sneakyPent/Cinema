module.exports = function(node, value) {
  var text = (node.textContent !== undefined ?
    'textContent' : 'innerText'
  )

  if (typeof value != 'undefined') {
    node[text] = value
  }

  return node[text]
}
