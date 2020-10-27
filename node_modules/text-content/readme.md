# text-content 
text-content is a cross-browser function for getting and setting the text value of a DOM element.

[![Build status](https://travis-ci.org/michaelrhodes/text-content.png?branch=master)](https://travis-ci.org/michaelrhodes/text-content)

[![Browser support](https://ci.testling.com/michaelrhodes/text-content.png)](https://ci.testling.com/michaelrhodes/text-content)

## Install
```
npm install text-content
```

### Example
``` js
var text = require('text-content')

var span = document.createElement('span')
text(span, 'Some text')

console.log(text(span))
// => Some text
```
It can also be used on the server with [mkdom](https://github.com/michaelrhodes/mkdom).

### License
[MIT](http://opensource.org/licenses/MIT)
