package furhatos.app.caproject.flow.main

object Recommender {
    fun processPurpose(text: String) {
        println("processing preferences!")
        //val purpose_list = khttp.post("http://localhost:8000/nlu/purpose", data = mapOf("text" to text))

        // Its a list of one element at this point, can adjust it for more
        val purpose_list = khttp.post("http://localhost:8000/nlu/keyword", data = mapOf("text" to text)) 

        // now we somehow feed it to the rec sys
        println("processed purpose!")
    }
    fun processPreferences(text: String) {
        println("processing preferences!")
        // TODO: connect this to Python preference engine

        val feature_list = khttp.post("http://localhost:8000/nlu/feature", data = mapOf("text" to text))

        // now we somehow feed it to the rec sys
        println("processed preferences!")
       
    }

    fun processUserResponse(artId: String, response: String) : Sentiment {
        println("processing sentiment on art: $artId , response: $response")

        //Connection to gaze part / stopping gaze evaluation
        val r = khttp.get("http://localhost:8000/gaze/stop")
        val attention = khttp.get("http://localhost:8000/gaze/getAttention")
        val sentiment = khttp.post("http://localhost:8000/nlu/sentiment", data = mapOf("text" to response))

        // now we somehow combine the two and update the graph

        // TODO: connect this to Python preference engine
        return Sentiment.POSITIVE
    }

    fun getArt() : Art {
        println("getting art!")
        // TODO: connect this to Python preference engine
        //Connection to gaze part / starting gaze evaluation
        val r = khttp.get("http://localhost:8000/gaze/start")

        return Art("coolart1", "/cool/art/image.png")
    }
}   