
  var port = chrome.runtime.connect({name: "knockknock"});


port.onMessage.addListener(function(msg) {

  if (msg.state == "Get me selected text"){
	port.postMessage({state:"Resp",selectedtext: window.getSelection().toString(), path:msg.path, url: document.URL}); 
}
});



