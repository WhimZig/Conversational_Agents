import FurhatGUI, { Furhat } from 'furhat-gui'

let furhat: Furhat = null

let pics = []

document.getElementById('folder').innerHTML="<h3>Arthos will show you amazing art in a second!</h3>"
//setting subcsriptions to get shit from the furhat skills
function setupSubscriptions() {

  console.log('setupSubscriptions')

  furhat.subscribe('furhatos.app.caproject.events.LoggingGui', (event) => {
    console.log('furhat said:', event.param1)
  })

  furhat.subscribe('furhatos.app.caproject.events.SetPics', (event) => {
    console.log('furhat said:', event.pics)
    setPicSelection(event.pics)
  })
  furhat.subscribe('furhatos.app.caproject.events.SetPicSolo', (event) => {
    console.log('furhat said:', event.pic)
    setSoloPic(event.pic)
  })

  
}


//Furhat code yoinked from github  https://github.com/FurhatRobotics/FurhatJSGUI
FurhatGUI()
  .then(connection => {

    furhat = connection
    console.log('received connection')

    furhat.onConnectionError((_connection: WebSocket, ev: globalThis.Event) => {
      console.error("Error occured while connecting to Furhat skill")
    })
    furhat.onConnectionClose(() => {
      console.warn("Connection with Furhat skill has been closed")
    })

    setupSubscriptions()
    //control ping so we know connection worked
    furhat.send({
      event_name: "LoggingPing",
    })
    console.log("Pinged Furhat skill")

  })
  .catch(console.error)

//Button to test everything
let debug=true
if(debug){
document.getElementById("debug-folder").innerHTML='<button type="button" id="pinging"> Ping! </button><button type="button" id="3pics"> All the pics! </button><button type="button" id="solopic"> Solo pic! </button>'
document.getElementById("pinging").addEventListener("click", () => { furhat.send({event_name:"LoggingPing"}) })
document.getElementById("solopic").addEventListener("click", () => { furhat.send({event_name:"SelectedPic",pic:"seascape_richter.jpg"}) })
document.getElementById("3pics").addEventListener("click", () => { furhat.send({event_name:"Showpics"}) })
}
// Setting 3 pic selection
function setPicSelection(input){
  console.log("Setting pic selection")
  let folder= document.getElementById("folder")
  let pic_names=input.split(',')
  let newHtml=""
  for(let i=0;i<pic_names.length;i++){
    newHtml+='<img class="art" id="pic-'+i+'" src="pics/'+pic_names[i]+'"/>'
  }
  folder.innerHTML = newHtml
  for(let i=0;i<pic_names.length;i++){
    document.getElementById("pic-"+i).addEventListener("click", () => {
      furhat.send({
        event_name: "SelectedPic",
        pic: pic_names[i],
      })
    })
  }
}

//setting solo pic
function setSoloPic(input){
  console.log('setting solo pic')
  let folder= document.getElementById("folder")
  folder.innerHTML ='<img class="art solo" src="pics/'+input+'"/>'
}