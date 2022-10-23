package furhatos.app.caproject.flow.main

data class Art (
    var id: String,
    var imagePath: String,
    var title: String = "",
    var artist: String = "",
    var medium: String = "",
    var timePeriod: String = ""
)