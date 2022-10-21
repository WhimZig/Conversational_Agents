package furhatos.app.caproject.flow.main

import furhatos.app.caproject.flow.Parent
import furhatos.flow.kotlin.*
import furhatos.nlu.common.No
import furhatos.nlu.common.Yes

var CURRENT_ART = Art("default", "/fake/image.png")

enum class Sentiment {
    POSITIVE, NEGATIVE
}

var sentiment = Sentiment.POSITIVE

val Purpose : State = state(Parent) {
    onEntry {
        furhat.ask("Hi ${NAME}, why are you looking for art?")
    }

    onResponse {
        println(it.text)
        furhat.say("Awesome, let me find some cool art for you!")
        Recommender.processPurpose(it.text)
        goto(Preference)
    }

}


val Preference : State = state(Parent) {
    onEntry {
        furhat.ask("Okay what kind of art are you interested in?")
    }

    onResponse {
        println(it.text)
        furhat.say("Awesome, let me find some cool art for you!")
        Recommender.processPreferences(it.text)
        goto(Showcase)
    }

}

val Showcase : State = state(Parent) {
    var art = Art("default", "/fake/image.png")
    onEntry {
        furhat.say("Here is my recommendation for you")
        art = Recommender.getArt()
        furhat.say(art.imagePath)
        furhat.say("This is ${art.artist}'s  ${art.title} on ${art.medium} from ${art.timePeriod}")
        furhat.say("What are your thoughts on the art?")
    }
    onResponse {
        println(it.text)
        sentiment = Recommender.processUserResponse(art.id, it.text)
        goto(ShowcaseMore)
    }
}

val ShowcaseMore : State = state(Parent) {
    onEntry {
        furhat.say("Would you like to explore more artworks?")
    }
    onResponse<Yes> {
        when(sentiment) {
            Sentiment.POSITIVE -> goto(ShowcaseSimilar)
            Sentiment.NEGATIVE -> goto(Preference)
        }
    }
    onResponse<No> {
        goto(Ending)
    }
}

val ShowcaseSimilar : State = state(Parent) {
    onEntry {
        furhat.say("Would you like to see  artworks similar to the previous?")
    }
    onResponse<Yes> {
        goto(Showcase)
    }
    onResponse<No> {
        goto(Preference)
    }
}


