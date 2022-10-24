/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/dist/";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 1);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Furhat = void 0;
const furhat_core_1 = __importDefault(__webpack_require__(2));
exports.Furhat = furhat_core_1.default;
let furhat;
let portNumber;
/**
 * FurhatGUI Function which sets up a connection to the furhat skill and gives
 * the furhat object to send and recieve events to the skill.
 * @return Promise that will return the promise with a `Furhat` obkect
 */
const FurhatGUI = () => new Promise((resolve, reject) => {
    window.fetch('/port', { method: 'GET' }) // eslint-disable-line no-undef
        .then(r => r.json())
        .then(({ address, port }) => {
        portNumber = port;
        furhat = new furhat_core_1.default(address, port, 'api');
        return furhat.init();
    })
        .then(() => {
        const senseSkillGuiEvent = {
            event_name: 'furhatos.event.senses.SenseSkillGUIConnected',
            port: portNumber,
        };
        furhat.send(senseSkillGuiEvent);
        resolve(furhat);
    })
        .catch((error) => reject(`Something went wrong: ${error}`));
});
exports.default = FurhatGUI;


/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _furhatGui = __webpack_require__(0);

var _furhatGui2 = _interopRequireDefault(_furhatGui);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var furhat = null;

var pics = [];

document.getElementById('folder').innerHTML = "<h3>Arthos will show you amazing art in a second!</h3>";
//setting subcsriptions to get shit from the furhat skills
function setupSubscriptions() {

  console.log('setupSubscriptions');

  furhat.subscribe('furhatos.app.caproject.events.LoggingGui', function (event) {
    console.log('furhat said:', event.param1);
  });

  furhat.subscribe('furhatos.app.caproject.events.SetPics', function (event) {
    console.log('furhat said:', event.pics);
    setPicSelection(event.pics);
  });
  furhat.subscribe('furhatos.app.caproject.events.SetPicSolo', function (event) {
    console.log('furhat said:', event.pic);
    setSoloPic(event.pic);
  });
}

//Furhat code yoinked from github  https://github.com/FurhatRobotics/FurhatJSGUI
(0, _furhatGui2.default)().then(function (connection) {

  furhat = connection;
  console.log('received connection');

  furhat.onConnectionError(function (_connection, ev) {
    console.error("Error occured while connecting to Furhat skill");
  });
  furhat.onConnectionClose(function () {
    console.warn("Connection with Furhat skill has been closed");
  });

  setupSubscriptions();
  //control ping so we know connection worked
  furhat.send({
    event_name: "LoggingPing"
  });
  console.log("Pinged Furhat skill");
}).catch(console.error);

//Button to test everything
var debug = true;
if (debug) {
  document.getElementById("debug-folder").innerHTML = '<button type="button" id="pinging"> Ping! </button><button type="button" id="3pics"> All the pics! </button><button type="button" id="solopic"> Solo pic! </button>';
  document.getElementById("pinging").addEventListener("click", function () {
    furhat.send({ event_name: "LoggingPing" });
  });
  document.getElementById("solopic").addEventListener("click", function () {
    furhat.send({ event_name: "SelectedPic", pic: "seascape_richter.jpg" });
  });
  document.getElementById("3pics").addEventListener("click", function () {
    furhat.send({ event_name: "Showpics" });
  });
}
// Setting 3 pic selection
function setPicSelection(input) {
  console.log("Setting pic selection");
  var folder = document.getElementById("folder");
  var pic_names = input.split(',');
  var newHtml = "";
  for (var i = 0; i < pic_names.length; i++) {
    newHtml += '<img class="art" id="pic-' + i + '" src="pics/imagesf2/' + pic_names[i] + '"/>';
  }
  folder.innerHTML = newHtml;

  var _loop = function _loop(_i) {
    document.getElementById("pic-" + _i).addEventListener("click", function () {
      furhat.send({
        event_name: "SelectedPic",
        pic: pic_names[_i]
      });
    });
  };

  for (var _i = 0; _i < pic_names.length; _i++) {
    _loop(_i);
  }
}

//setting solo pic
function setSoloPic(input) {
  console.log('setting solo pic');
  var folder = document.getElementById("folder");
  folder.innerHTML = '<img class="art solo" src="pics/imagesf2/' + input + '"/>';
}

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Furhat main class. Maintains the websocket connection to furhatOS and
 * has methods to send events, subscribe to events and helper methods such as say,
 * gesture, etc.
 *
 * @param domain IP Address for furhatOS - localhost if SDK.
 * @param port port for RealTimeAPI module of furhatOS.
 * @param route route for RealTimeAPI module of furhatOS.
 */
class Furhat {
    constructor(domain, port, route) {
        this.eventFunctions = {};
        this.domain = domain;
        this.port = port;
        this.route = route;
    }
    /**
     * Initializes the connection and return a promise. Await for the promise to resolve before
     * using the object
     */
    init() {
        return new Promise((resolve, reject) => {
            this.socket = new WebSocket(`ws://${this.domain}:${this.port}/${this.route}`);
            this.socket.onopen = () => {
                resolve({ error: false, message: "Success" });
            };
            this.socket.onmessage = (message) => {
                const event = JSON.parse(message.data);
                // If a callback is available then call it
                this.eventFunctions[event.event_name] !== undefined &&
                    this.eventFunctions[event.event_name](event);
            };
            this.socket.onerror = () => {
                reject({ error: true, message: "Error while opening socket" });
            };
        });
    }
    /**
     * Method to set a callback that will be triggered `onerror` of the underlying websocket
     * @param callback Callback function to be trigger on WebSocket connection error
     */
    onConnectionError(callback) { this.socket && (this.socket.onerror = callback); }
    /**
     * Method to set a callback that will be triggered `onclose` of the underlying websocket
     * @param callback Callback function to be trigger on WebSocket connection close
     */
    onConnectionClose(callback) { this.socket && (this.socket.onclose = callback); }
    /**
     * Sends an event to furhatOS
     * @param event Object containing the event. Mandtory to have event_name parameter in the object
     */
    send(event) {
        var _a, _b, _c;
        if (((_a = this.socket) === null || _a === void 0 ? void 0 : _a.readyState) === 2 || ((_b = this.socket) === null || _b === void 0 ? void 0 : _b.readyState) === 3) {
            console.warn("Cannot send event. Socket is not ready.");
            return false;
        }
        else if (((_c = this.socket) === null || _c === void 0 ? void 0 : _c.readyState) === 1) {
            this.socket.send(JSON.stringify(event));
            return true;
        }
        return false;
    }
    /**
     * Subscribes to the given event and triggers the supplied callback on event
     * @param eventName Name of the event to subscribe
     * @param callback Function which needs to be triggered when the given event is recieved
     * @param dontSend [Optional] [false by default] Boolean which determines wether to send
     * the subscribe event or not. use it to set callbacks for event that are already subscribed to,
     * for instance with group subscriptions
     */
    subscribe(eventName, callback, dontSend = false) {
        const event = { event_name: 'furhatos.event.actions.ActionRealTimeAPISubscribe', name: eventName };
        this.eventFunctions[eventName] = callback;
        if (!dontSend) {
            return this.send(event);
        }
        return true;
    }
    /**
     * Subscribes to the given event group
     * @param groupNumber Number(Assigned ENUM) of the group that needs to be subscribed to
     */
    subscribeGroup(groupNumber) {
        const event = { event_name: 'furhatos.event.actions.ActionRealTimeAPISubscribe', group: groupNumber };
        return this.send(event);
    }
    /**
     * Says a given text
     * @param text Text which needs to be said by Furhat
     */
    say(text) {
        const event = { event_name: 'furhatos.event.actions.ActionSpeech', text };
        return this.send(event);
    }
    /**
     * Stimulates the speech of a user in the interaction space
     * @param text Text which needs to be said by the user
     */
    userSpeech(text) {
        const event = { event_name: 'furhatos.event.senses.SenseTypingEnd', messageText: text };
        return this.send(event);
    }
    /**
     * Stimulates SenseSpeechStart event. Can be used to stimulate user speech via typing
     */
    userSpeechStart() {
        const event = { event_name: 'furhatos.event.senses.SenseTypingStart' };
        return this.send(event);
    }
    /**
     * Performs the given gesture
     * @param name Name of the gesture that needs to be performed
     */
    gesture(name) {
        const event = { event_name: 'furhatos.event.actions.ActionGesture', name };
        return this.send(event);
    }
}
exports.default = Furhat;


/***/ })
/******/ ]);
//# sourceMappingURL=bundle.js.map