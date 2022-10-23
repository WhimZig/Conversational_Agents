package furhatos.app.caproject.flow.main

object Recommender {
    fun processPurpose(text: String) {
        println("processing purpose!")
        //val purpose_list = khttp.post("http://localhost:8000/nlu/purpose", data = mapOf("text" to text))

        // Its a list of one element at this point, can adjust it for more
        val purpose_list = khttp.post("http://localhost:8000/nlu/keyword", data = mapOf("text" to text)).purposes


        println("processed purpose!")
    }
    fun processPreferences(text: String) {
        println("processing preferences!")

        val feature_list = khttp.post("http://localhost:8000/nlu/feature", data = mapOf("text" to text)).features

        for (feature in feature_list) {
            khttp.post("http://localhost:8000/mem/topic", data = mapOf("text" to feature))
        }

        println("processed preferences!")
       
    }

    fun processUserResponse(artId: String, response: String) : Sentiment {
        println("processing sentiment on art: $artId , response: $response")

        //Connection to gaze part / stopping gaze evaluation
        val r = khttp.get("http://localhost:8000/gaze/stop")
        val attention = khttp.get("http://localhost:8000/gaze/getAttention").attention
        val sentiment = khttp.post("http://localhost:8000/nlu/sentiment", data = mapOf("text" to response)).sentiment
        // if there is a problem here put the attribute calling somewhere after the function
        val combined_score = 0.5 * sentiment + 0.5 * attention * sentiment

        khttp.post("http://localhost:8000/mem/painting_score", data = mapOf("text" to artId, "sentiment" to combined_score))
        return Sentiment.POSITIVE
    }

    fun getArt() : Art {
        println("getting art!")
        // TODO: connect this to Python preference engine
        //Connection to gaze part / starting gaze evaluation
        val r = khttp.get("http://localhost:8000/gaze/start")

        val art_name = khttp.get("http://localhost:8000/mem/painting_recommend").painting

        return Art("coolart1", "/cool/art/image.png")
    }
}   