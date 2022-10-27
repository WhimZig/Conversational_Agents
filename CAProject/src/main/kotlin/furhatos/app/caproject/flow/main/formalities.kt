package furhatos.app.caproject.flow.main

import furhatos.app.caproject.flow.Parent
import furhatos.flow.kotlin.*
import furhatos.nlu.common.No
import furhatos.nlu.common.PersonName
import furhatos.nlu.common.Yes

var NAME  = ""

val Greeting : State = state(Parent) {
    onEntry {
        Recommender.wipe()
        furhat.say("Hello my name is Arthur the art recommender robot")
        furhat.ask("Whats your name?")

    }

    onResponse<PersonName> {
        NAME = it.intent.toString()
        println("customer name is $NAME")
        goto(Purpose)
    }

    onResponse {
        goto(Purpose)
    }

}

val Ending : State = state(Parent) {
    onEntry {
        Recommender.wipe()
        furhat.ask("Are you satisfied with my recommendation?")
    }
    onResponse<Yes> {
        furhat.say("Glad to hear that! Hope to see you again soon. Goodbye.")
    }
    onResponse<No> {
        furhat.say("I'm sorry to hear that. I hope I can do a better job next time, goodbye.")
    }
}
