package furhatos.app.caproject.flow

import furhatos.flow.kotlin.*
import furhatos.app.caproject.flow.main.Idle

import furhatos.app.caproject.events.*
import furhatos.event.senses.SenseSkillGUIConnected
import furhatos.skills.HostedGUI

val default_gui = HostedGUI("FH-GUI","assets/web_gui",55000)


val Parent: State = state {

    onEvent("LoggingPing"){
        println("Got Pinged by GUI!")
    }

    onEvent("SelectedPic"){
        println("Selected Pic: "+it.get("pic"))
        send(SetPicSolo(it.get("pic").toString()))
        //TODO
    }

    onEvent("Showpics"){
        println("pls noods")
        send(SetPics("painting1_richter.jpg,seascape_richter.jpg,womanchild_richter.jpg"))
        //TODO
    }

    onUserLeave(instant = true) {
        when {
            users.count == 0 -> goto(Idle)
            it == users.current -> furhat.attend(users.other)
        }
    }

    onEvent<SenseSkillGUIConnected> {
        println("Trying to connect. \nExpecting a ping back!")
        send(LoggingGui("bittebittebitte"))
    }

    onUserEnter(instant = true) {
        furhat.glance(it)
    }
}