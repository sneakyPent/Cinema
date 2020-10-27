/**
 * Require the module at `name`.
 *
 * @param {String} name
 * @return {Object} exports
 * @api public
 */

function require(name) {
  var module = require.modules[name];
  if (!module) throw new Error('failed to require "' + name + '"');

  if (!('exports' in module) && typeof module.definition === 'function') {
    module.client = module.component = true;
    module.definition.call(this, module.exports = {}, module);
    delete module.definition;
  }

  return module.exports;
}

/**
 * Meta info, accessible in the global scope unless you use AMD option.
 */

require.loader = 'component';

/**
 * Internal helper object, contains a sorting function for semantiv versioning
 */
require.helper = {};
require.helper.semVerSort = function(a, b) {
  var aArray = a.version.split('.');
  var bArray = b.version.split('.');
  for (var i=0; i<aArray.length; ++i) {
    var aInt = parseInt(aArray[i], 10);
    var bInt = parseInt(bArray[i], 10);
    if (aInt === bInt) {
      var aLex = aArray[i].substr((""+aInt).length);
      var bLex = bArray[i].substr((""+bInt).length);
      if (aLex === '' && bLex !== '') return 1;
      if (aLex !== '' && bLex === '') return -1;
      if (aLex !== '' && bLex !== '') return aLex > bLex ? 1 : -1;
      continue;
    } else if (aInt > bInt) {
      return 1;
    } else {
      return -1;
    }
  }
  return 0;
}

/**
 * Find and require a module which name starts with the provided name.
 * If multiple modules exists, the highest semver is used. 
 * This function can only be used for remote dependencies.

 * @param {String} name - module name: `user~repo`
 * @param {Boolean} returnPath - returns the canonical require path if true, 
 *                               otherwise it returns the epxorted module
 */
require.latest = function (name, returnPath) {
  function showError(name) {
    throw new Error('failed to find latest module of "' + name + '"');
  }
  // only remotes with semvers, ignore local files conataining a '/'
  var versionRegexp = /(.*)~(.*)@v?(\d+\.\d+\.\d+[^\/]*)$/;
  var remoteRegexp = /(.*)~(.*)/;
  if (!remoteRegexp.test(name)) showError(name);
  var moduleNames = Object.keys(require.modules);
  var semVerCandidates = [];
  var otherCandidates = []; // for instance: name of the git branch
  for (var i=0; i<moduleNames.length; i++) {
    var moduleName = moduleNames[i];
    if (new RegExp(name + '@').test(moduleName)) {
        var version = moduleName.substr(name.length+1);
        var semVerMatch = versionRegexp.exec(moduleName);
        if (semVerMatch != null) {
          semVerCandidates.push({version: version, name: moduleName});
        } else {
          otherCandidates.push({version: version, name: moduleName});
        } 
    }
  }
  if (semVerCandidates.concat(otherCandidates).length === 0) {
    showError(name);
  }
  if (semVerCandidates.length > 0) {
    var module = semVerCandidates.sort(require.helper.semVerSort).pop().name;
    if (returnPath === true) {
      return module;
    }
    return require(module);
  }
  // if the build contains more than one branch of the same module
  // you should not use this funciton
  var module = otherCandidates.sort(function(a, b) {return a.name > b.name})[0].name;
  if (returnPath === true) {
    return module;
  }
  return require(module);
}

/**
 * Registered modules.
 */

require.modules = {};

/**
 * Register module at `name` with callback `definition`.
 *
 * @param {String} name
 * @param {Function} definition
 * @api private
 */

require.register = function (name, definition) {
  require.modules[name] = {
    definition: definition
  };
};

/**
 * Define a module's exports immediately with `exports`.
 *
 * @param {String} name
 * @param {Generic} exports
 * @api private
 */

require.define = function (name, exports) {
  require.modules[name] = {
    exports: exports
  };
};
require.register("yields~fmt@0.0.2", Function("exports, module",
"\n\
/**\n\
 * Export `fmt`\n\
 */\n\
\n\
module.exports = fmt;\n\
\n\
/**\n\
 * Formatters\n\
 */\n\
\n\
fmt.o = JSON.stringify;\n\
fmt.s = String;\n\
fmt.d = parseInt;\n\
\n\
/**\n\
 * Format the given `str`.\n\
 *\n\
 * @param {String} str\n\
 * @param {...} args\n\
 * @return {String}\n\
 * @api public\n\
 */\n\
\n\
function fmt(str){\n\
  var args = [].slice.call(arguments, 1);\n\
  var j = 0;\n\
\n\
  return str.replace(/%([a-z])/gi, function(_, f){\n\
    return fmt[f]\n\
      ? fmt[f](args[j++])\n\
      : _ + f;\n\
  });\n\
}\n\
\n\
//# sourceURL=components/yields/fmt/0.0.2/index.js"
));

require.modules["yields-fmt"] = require.modules["yields~fmt@0.0.2"];
require.modules["yields~fmt"] = require.modules["yields~fmt@0.0.2"];
require.modules["fmt"] = require.modules["yields~fmt@0.0.2"];


require.register("component~stack@0.0.1", Function("exports, module",
"\n\
/**\n\
 * Expose `stack()`.\n\
 */\n\
\n\
module.exports = stack;\n\
\n\
/**\n\
 * Return the stack.\n\
 *\n\
 * @return {Array}\n\
 * @api public\n\
 */\n\
\n\
function stack() {\n\
  var orig = Error.prepareStackTrace;\n\
  Error.prepareStackTrace = function(_, stack){ return stack; };\n\
  var err = new Error;\n\
  Error.captureStackTrace(err, arguments.callee);\n\
  var stack = err.stack;\n\
  Error.prepareStackTrace = orig;\n\
  return stack;\n\
}\n\
//# sourceURL=components/component/stack/0.0.1/index.js"
));

require.modules["component-stack"] = require.modules["component~stack@0.0.1"];
require.modules["component~stack"] = require.modules["component~stack@0.0.1"];
require.modules["stack"] = require.modules["component~stack@0.0.1"];


require.register("jkroso~type@1.1.0", Function("exports, module",
"\n\
var toString = {}.toString\n\
var DomNode = typeof window != 'undefined'\n\
  ? window.Node\n\
  : Function\n\
\n\
/**\n\
 * Return the type of `val`.\n\
 *\n\
 * @param {Mixed} val\n\
 * @return {String}\n\
 * @api public\n\
 */\n\
\n\
module.exports = exports = function(x){\n\
  var type = typeof x\n\
  if (type != 'object') return type\n\
  type = types[toString.call(x)]\n\
  if (type) return type\n\
  if (x instanceof DomNode) switch (x.nodeType) {\n\
    case 1:  return 'element'\n\
    case 3:  return 'text-node'\n\
    case 9:  return 'document'\n\
    case 11: return 'document-fragment'\n\
    default: return 'dom-node'\n\
  }\n\
}\n\
\n\
var types = exports.types = {\n\
  '[object Function]': 'function',\n\
  '[object Date]': 'date',\n\
  '[object RegExp]': 'regexp',\n\
  '[object Arguments]': 'arguments',\n\
  '[object Array]': 'array',\n\
  '[object String]': 'string',\n\
  '[object Null]': 'null',\n\
  '[object Undefined]': 'undefined',\n\
  '[object Number]': 'number',\n\
  '[object Boolean]': 'boolean',\n\
  '[object Object]': 'object',\n\
  '[object Text]': 'text-node',\n\
  '[object Uint8Array]': 'bit-array',\n\
  '[object Uint16Array]': 'bit-array',\n\
  '[object Uint32Array]': 'bit-array',\n\
  '[object Uint8ClampedArray]': 'bit-array',\n\
  '[object Error]': 'error',\n\
  '[object FormData]': 'form-data',\n\
  '[object File]': 'file',\n\
  '[object Blob]': 'blob'\n\
}\n\
\n\
//# sourceURL=components/jkroso/type/1.1.0/index.js"
));

require.modules["jkroso-type"] = require.modules["jkroso~type@1.1.0"];
require.modules["jkroso~type"] = require.modules["jkroso~type@1.1.0"];
require.modules["type"] = require.modules["jkroso~type@1.1.0"];


require.register("jkroso~equals@1.0.0", Function("exports, module",
"var type = require('jkroso~type@1.1.0')\n\
\n\
// (any, any, [array]) -> boolean\n\
function equal(a, b, memos){\n\
  // All identical values are equivalent\n\
  if (a === b) return true\n\
  var fnA = types[type(a)]\n\
  var fnB = types[type(b)]\n\
  return fnA && fnA === fnB\n\
    ? fnA(a, b, memos)\n\
    : false\n\
}\n\
\n\
var types = {}\n\
\n\
// (Number) -> boolean\n\
types.number = function(a, b){\n\
  return a !== a && b !== b/*Nan check*/\n\
}\n\
\n\
// (function, function, array) -> boolean\n\
types['function'] = function(a, b, memos){\n\
  return a.toString() === b.toString()\n\
    // Functions can act as objects\n\
    && types.object(a, b, memos)\n\
    && equal(a.prototype, b.prototype)\n\
}\n\
\n\
// (date, date) -> boolean\n\
types.date = function(a, b){\n\
  return +a === +b\n\
}\n\
\n\
// (regexp, regexp) -> boolean\n\
types.regexp = function(a, b){\n\
  return a.toString() === b.toString()\n\
}\n\
\n\
// (DOMElement, DOMElement) -> boolean\n\
types.element = function(a, b){\n\
  return a.outerHTML === b.outerHTML\n\
}\n\
\n\
// (textnode, textnode) -> boolean\n\
types.textnode = function(a, b){\n\
  return a.textContent === b.textContent\n\
}\n\
\n\
// decorate `fn` to prevent it re-checking objects\n\
// (function) -> function\n\
function memoGaurd(fn){\n\
  return function(a, b, memos){\n\
    if (!memos) return fn(a, b, [])\n\
    var i = memos.length, memo\n\
    while (memo = memos[--i]) {\n\
      if (memo[0] === a && memo[1] === b) return true\n\
    }\n\
    return fn(a, b, memos)\n\
  }\n\
}\n\
\n\
types['arguments'] =\n\
types.array = memoGaurd(arrayEqual)\n\
\n\
// (array, array, array) -> boolean\n\
function arrayEqual(a, b, memos){\n\
  var i = a.length\n\
  if (i !== b.length) return false\n\
  memos.push([a, b])\n\
  while (i--) {\n\
    if (!equal(a[i], b[i], memos)) return false\n\
  }\n\
  return true\n\
}\n\
\n\
types.object = memoGaurd(objectEqual)\n\
\n\
// (object, object, array) -> boolean\n\
function objectEqual(a, b, memos) {\n\
  if (typeof a.equal == 'function') {\n\
    memos.push([a, b])\n\
    return a.equal(b, memos)\n\
  }\n\
  var ka = getEnumerableProperties(a)\n\
  var kb = getEnumerableProperties(b)\n\
  var i = ka.length\n\
\n\
  // same number of properties\n\
  if (i !== kb.length) return false\n\
\n\
  // although not necessarily the same order\n\
  ka.sort()\n\
  kb.sort()\n\
\n\
  // cheap key test\n\
  while (i--) if (ka[i] !== kb[i]) return false\n\
\n\
  // remember\n\
  memos.push([a, b])\n\
\n\
  // iterate again this time doing a thorough check\n\
  i = ka.length\n\
  while (i--) {\n\
    var key = ka[i]\n\
    if (!equal(a[key], b[key], memos)) return false\n\
  }\n\
\n\
  return true\n\
}\n\
\n\
// (object) -> array\n\
function getEnumerableProperties (object) {\n\
  var result = []\n\
  for (var k in object) if (k !== 'constructor') {\n\
    result.push(k)\n\
  }\n\
  return result\n\
}\n\
\n\
module.exports = equal\n\
\n\
//# sourceURL=components/jkroso/equals/1.0.0/index.js"
));

require.modules["jkroso-equals"] = require.modules["jkroso~equals@1.0.0"];
require.modules["jkroso~equals"] = require.modules["jkroso~equals@1.0.0"];
require.modules["equals"] = require.modules["jkroso~equals@1.0.0"];


require.register("component~assert@0.5.0", Function("exports, module",
"\n\
/**\n\
 * Module dependencies.\n\
 */\n\
\n\
var equals = require('jkroso~equals@1.0.0');\n\
var fmt = require('yields~fmt@0.0.2');\n\
var stack = require('component~stack@0.0.1');\n\
\n\
/**\n\
 * Assert `expr` with optional failure `msg`.\n\
 *\n\
 * @param {Mixed} expr\n\
 * @param {String} [msg]\n\
 * @api public\n\
 */\n\
\n\
module.exports = exports = function (expr, msg) {\n\
  if (expr) return;\n\
  throw error(msg || message());\n\
};\n\
\n\
/**\n\
 * Assert `actual` is weak equal to `expected`.\n\
 *\n\
 * @param {Mixed} actual\n\
 * @param {Mixed} expected\n\
 * @param {String} [msg]\n\
 * @api public\n\
 */\n\
\n\
exports.equal = function (actual, expected, msg) {\n\
  if (actual == expected) return;\n\
  throw error(msg || fmt('Expected %o to equal %o.', actual, expected), actual, expected);\n\
};\n\
\n\
/**\n\
 * Assert `actual` is not weak equal to `expected`.\n\
 *\n\
 * @param {Mixed} actual\n\
 * @param {Mixed} expected\n\
 * @param {String} [msg]\n\
 * @api public\n\
 */\n\
\n\
exports.notEqual = function (actual, expected, msg) {\n\
  if (actual != expected) return;\n\
  throw error(msg || fmt('Expected %o not to equal %o.', actual, expected));\n\
};\n\
\n\
/**\n\
 * Assert `actual` is deep equal to `expected`.\n\
 *\n\
 * @param {Mixed} actual\n\
 * @param {Mixed} expected\n\
 * @param {String} [msg]\n\
 * @api public\n\
 */\n\
\n\
exports.deepEqual = function (actual, expected, msg) {\n\
  if (equals(actual, expected)) return;\n\
  throw error(msg || fmt('Expected %o to deeply equal %o.', actual, expected), actual, expected);\n\
};\n\
\n\
/**\n\
 * Assert `actual` is not deep equal to `expected`.\n\
 *\n\
 * @param {Mixed} actual\n\
 * @param {Mixed} expected\n\
 * @param {String} [msg]\n\
 * @api public\n\
 */\n\
\n\
exports.notDeepEqual = function (actual, expected, msg) {\n\
  if (!equals(actual, expected)) return;\n\
  throw error(msg || fmt('Expected %o not to deeply equal %o.', actual, expected));\n\
};\n\
\n\
/**\n\
 * Assert `actual` is strict equal to `expected`.\n\
 *\n\
 * @param {Mixed} actual\n\
 * @param {Mixed} expected\n\
 * @param {String} [msg]\n\
 * @api public\n\
 */\n\
\n\
exports.strictEqual = function (actual, expected, msg) {\n\
  if (actual === expected) return;\n\
  throw error(msg || fmt('Expected %o to strictly equal %o.', actual, expected), actual, expected);\n\
};\n\
\n\
/**\n\
 * Assert `actual` is not strict equal to `expected`.\n\
 *\n\
 * @param {Mixed} actual\n\
 * @param {Mixed} expected\n\
 * @param {String} [msg]\n\
 * @api public\n\
 */\n\
\n\
exports.notStrictEqual = function (actual, expected, msg) {\n\
  if (actual !== expected) return;\n\
  throw error(msg || fmt('Expected %o not to strictly equal %o.', actual, expected));\n\
};\n\
\n\
/**\n\
 * Assert `block` throws an `error`.\n\
 *\n\
 * @param {Function} block\n\
 * @param {Function} [error]\n\
 * @param {String} [msg]\n\
 * @api public\n\
 */\n\
\n\
exports.throws = function (block, err, msg) {\n\
  var threw;\n\
  try {\n\
    block();\n\
  } catch (e) {\n\
    threw = e;\n\
  }\n\
\n\
  if (!threw) throw error(msg || fmt('Expected %s to throw an error.', block.toString()));\n\
  if (err && !(threw instanceof err)) {\n\
    throw error(msg || fmt('Expected %s to throw an %o.', block.toString(), err));\n\
  }\n\
};\n\
\n\
/**\n\
 * Assert `block` doesn't throw an `error`.\n\
 *\n\
 * @param {Function} block\n\
 * @param {Function} [error]\n\
 * @param {String} [msg]\n\
 * @api public\n\
 */\n\
\n\
exports.doesNotThrow = function (block, err, msg) {\n\
  var threw;\n\
  try {\n\
    block();\n\
  } catch (e) {\n\
    threw = e;\n\
  }\n\
\n\
  if (threw) throw error(msg || fmt('Expected %s not to throw an error.', block.toString()));\n\
  if (err && (threw instanceof err)) {\n\
    throw error(msg || fmt('Expected %s not to throw an %o.', block.toString(), err));\n\
  }\n\
};\n\
\n\
/**\n\
 * Create a message from the call stack.\n\
 *\n\
 * @return {String}\n\
 * @api private\n\
 */\n\
\n\
function message() {\n\
  if (!Error.captureStackTrace) return 'assertion failed';\n\
  var callsite = stack()[2];\n\
  var fn = callsite.getFunctionName();\n\
  var file = callsite.getFileName();\n\
  var line = callsite.getLineNumber() - 1;\n\
  var col = callsite.getColumnNumber() - 1;\n\
  var src = get(file);\n\
  line = src.split('\\n\
')[line].slice(col);\n\
  var m = line.match(/assert\\((.*)\\)/);\n\
  return m && m[1].trim();\n\
}\n\
\n\
/**\n\
 * Load contents of `script`.\n\
 *\n\
 * @param {String} script\n\
 * @return {String}\n\
 * @api private\n\
 */\n\
\n\
function get(script) {\n\
  var xhr = new XMLHttpRequest;\n\
  xhr.open('GET', script, false);\n\
  xhr.send(null);\n\
  return xhr.responseText;\n\
}\n\
\n\
/**\n\
 * Error with `msg`, `actual` and `expected`.\n\
 *\n\
 * @param {String} msg\n\
 * @param {Mixed} actual\n\
 * @param {Mixed} expected\n\
 * @return {Error}\n\
 */\n\
\n\
function error(msg, actual, expected){\n\
  var err = new Error(msg);\n\
  err.showDiff = 3 == arguments.length;\n\
  err.actual = actual;\n\
  err.expected = expected;\n\
  return err;\n\
}\n\
\n\
//# sourceURL=components/component/assert/0.5.0/index.js"
));

require.modules["component-assert"] = require.modules["component~assert@0.5.0"];
require.modules["component~assert"] = require.modules["component~assert@0.5.0"];
require.modules["assert"] = require.modules["component~assert@0.5.0"];


require.register("domify", Function("exports, module",
"\n\
/**\n\
 * Expose `parse`.\n\
 */\n\
\n\
module.exports = parse;\n\
\n\
/**\n\
 * Tests for browser support.\n\
 */\n\
\n\
var div = document.createElement('div');\n\
// Setup\n\
div.innerHTML = '  <link/><table></table><a href=\"/a\">a</a><input type=\"checkbox\"/>';\n\
// Make sure that link elements get serialized correctly by innerHTML\n\
// This requires a wrapper element in IE\n\
var innerHTMLBug = !div.getElementsByTagName('link').length;\n\
div = undefined;\n\
\n\
/**\n\
 * Wrap map from jquery.\n\
 */\n\
\n\
var map = {\n\
  legend: [1, '<fieldset>', '</fieldset>'],\n\
  tr: [2, '<table><tbody>', '</tbody></table>'],\n\
  col: [2, '<table><tbody></tbody><colgroup>', '</colgroup></table>'],\n\
  // for script/link/style tags to work in IE6-8, you have to wrap\n\
  // in a div with a non-whitespace character in front, ha!\n\
  _default: innerHTMLBug ? [1, 'X<div>', '</div>'] : [0, '', '']\n\
};\n\
\n\
map.td =\n\
map.th = [3, '<table><tbody><tr>', '</tr></tbody></table>'];\n\
\n\
map.option =\n\
map.optgroup = [1, '<select multiple=\"multiple\">', '</select>'];\n\
\n\
map.thead =\n\
map.tbody =\n\
map.colgroup =\n\
map.caption =\n\
map.tfoot = [1, '<table>', '</table>'];\n\
\n\
map.polyline =\n\
map.ellipse =\n\
map.polygon =\n\
map.circle =\n\
map.text =\n\
map.line =\n\
map.path =\n\
map.rect =\n\
map.g = [1, '<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\">','</svg>'];\n\
\n\
/**\n\
 * Parse `html` and return a DOM Node instance, which could be a TextNode,\n\
 * HTML DOM Node of some kind (<div> for example), or a DocumentFragment\n\
 * instance, depending on the contents of the `html` string.\n\
 *\n\
 * @param {String} html - HTML string to \"domify\"\n\
 * @param {Document} doc - The `document` instance to create the Node for\n\
 * @return {DOMNode} the TextNode, DOM Node, or DocumentFragment instance\n\
 * @api private\n\
 */\n\
\n\
function parse(html, doc) {\n\
  if ('string' != typeof html) throw new TypeError('String expected');\n\
\n\
  // default to the global `document` object\n\
  if (!doc) doc = document;\n\
\n\
  // tag name\n\
  var m = /<([\\w:]+)/.exec(html);\n\
  if (!m) return doc.createTextNode(html);\n\
\n\
  html = html.replace(/^\\s+|\\s+$/g, ''); // Remove leading/trailing whitespace\n\
\n\
  var tag = m[1];\n\
\n\
  // body support\n\
  if (tag == 'body') {\n\
    var el = doc.createElement('html');\n\
    el.innerHTML = html;\n\
    return el.removeChild(el.lastChild);\n\
  }\n\
\n\
  // wrap map\n\
  var wrap = map[tag] || map._default;\n\
  var depth = wrap[0];\n\
  var prefix = wrap[1];\n\
  var suffix = wrap[2];\n\
  var el = doc.createElement('div');\n\
  el.innerHTML = prefix + html + suffix;\n\
  while (depth--) el = el.lastChild;\n\
\n\
  // one element\n\
  if (el.firstChild == el.lastChild) {\n\
    return el.removeChild(el.firstChild);\n\
  }\n\
\n\
  // several elements\n\
  var fragment = doc.createDocumentFragment();\n\
  while (el.firstChild) {\n\
    fragment.appendChild(el.removeChild(el.firstChild));\n\
  }\n\
\n\
  return fragment;\n\
}\n\
\n\
//# sourceURL=index.js"
));

require.modules["domify"] = require.modules["domify"];


require("domify");
