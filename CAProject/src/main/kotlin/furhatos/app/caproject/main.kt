package furhatos.app.caproject

import furhatos.app.caproject.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class CaprojectSkill : Skill() {


    override fun start() {
        Flow().run(Init)
    }
}
fun main(args: Array<String>) {
    Skill.main(args)
}
