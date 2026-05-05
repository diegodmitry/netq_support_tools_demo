/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


onmessage = function(event) {
  importScripts('highlight.pack.js');
  var result = self.hljs.highlightAuto(event.data);
  postMessage(result.value);
}