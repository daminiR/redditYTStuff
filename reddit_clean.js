function removeGradient() {
    //if(isShort === true){
    const address = document.querySelector("._1OVBBWLtHoSPfGCRaPzpTf._3nSp9cdBpqL13CqjdMr2L_._2udhMC-jldHp_EpAuBeSR1.PaJBYLqPf_Gie2aZntVQ7._2OVNlZuUd8L9v0yVECZ2iA");
    address.style.marginRight = 0
    const eddted_ago = document.querySelectorAll("._2ETuFsVzMBxiHia6HfJCTQ._18WUrfxbke5CjwIjhXu6C-");
    for (let item of eddted_ago) {
        item.innerText = ""
    }
    const items = document.querySelectorAll(".TmlaIdEplCzZ0F1aRGYQh");
    const items_comminute_bar = document.querySelectorAll("._3Kd8DQpBIbsr5E1JcrMFTY._1tvThPWQpORoc2taKebHxs");
    const items_archive = document.querySelectorAll("._1EjIqPTCvhReSe3IjZptiB._1DUKbp8va6vxOv9zemBDBi");
    for (let item of items) {
         item.remove();
    }
    for (let item of items_comminute_bar) {
         item.remove();
    }
    for (let item of items_archive) {
         item.remove();
    }
    const comment_deleted_by_user = document.querySelectorAll(".-Xcv3XBXmgiY2X5RqaPbO._1S45SPAIb30fsXtEcKPSdt._3c9Go6433BnvYx8_7MkPnt._3LqBzV8aCO9tge99jHiUGy._2k27lgIDltx9kOzVGXt48i");

    if (comment_deleted_by_user != null ){

    for (let item of comment_deleted_by_user) {
            item.parentElement.parentElement.remove()
    }
    }
    const top1 = document.querySelector("._2vkeRJojnV7cb9pMlPHy7d ")
    top1?.remove();
    const top2 = document.querySelector("._2L5G9B5yaoqW3IegiYN-FL")
    top2?.remove();
    const top3 = document.querySelector("._1gVVmSnHZpkUgVShsn7-ua")
    top3?.remove();
    //const nsfw = document.querySelectorAll("._3xX726aBn29LDbsDtzr_6E._1Ap4F5maDtT1E1YuCiaO0r.D3IL3FD0RFy_mkKLPwL4")
    //for (let item of nsfw) {
         //item.remove()
    //}

     //this class is wrong id , this remove first comment -> change this to creect one
    //const remove_by_mod = document.querySelector("._3yx4Dn0W3Yunucf5sVJeFU")
    //remove_by_mod?.remove();
    var deleted_mod = document.querySelectorAll("div[data-testid='post-comment-header-deleted']");
    for (let item of deleted_mod) {
         item.parentElement.parentElement.remove()
    }
    const blocked = document.querySelector(".jf95ZrrjIs2i--Ud8Kvb7._1DUKbp8va6vxOv9zemBDBi")
    blocked?.remove();
    const mod_comment = document.querySelector(".LWgI-A6rN9Wajn1VLxu2A._3AgEmWP1qkCB8nds7LhzEB")
    mod_comment?.parentElement.parentElement.parentElement.parentElement.remove()
    const upvotes = document.querySelector("._23h0-EcaBUorIHC-JZyh6J")
    upvotes?.remove();
    const title_posted = document.querySelector("._14-YvdFiW5iVvfe5wdgmET")
    title_posted?.remove();
    const title_chip = document.querySelector("._2fiIRtMpITeCAzXc4cANKp._1mK-LVHGTTlcFpMsjItjYJ")
    title_chip?.remove();
    const post_edits = document.querySelector("._1hwEKkB_38tIoal6fcdrt9")
    post_edits?.remove();
    const reply_block = document.querySelector("._1r4smTyOEZFO91uFIdWW6T.aUM8DQ_Nz5wL0EJc_wte6")
    reply_block?.remove();
    const suggested_block = document.querySelector("._2ulKn_zs7Y3LWsOqoFLHPo")
    suggested_block?.remove();
    const add_block = document.querySelector(".Pbz3gpOA6rvqdYoX_pOjn")
    add_block?.remove();
    const cont_block = document.querySelectorAll("._3ndawrYzcvjHPJFYUHijfP ")
    for (let item of cont_block) {
    item.remove();
    }
    const reply_block2 = document.querySelectorAll("._2HYsucNpMdUpYlGBMviq8M._23013peWUhznY89KuYPZKv")
    for (let item of reply_block2) {
    item.remove();
    }
    const awards = document.querySelectorAll(".n08B7PrU01wzgZYIh-s7N")
    for (let item of awards) {
    item.remove();
    }
    const red_shadow = document.querySelectorAll("._3VH2iGVh92XtlKq0-eVoEN")
    for (let item of red_shadow) {
    item.remove();
    }
    const chips = document.querySelectorAll("._3w527zTLhXkd08MyacMV9H")
    for (let item of chips) {
    item.remove();
    }
    const comment_button = document.querySelectorAll(".cmR5BF4NpBUm3DBMZCmJS._1cubpGNEaCAVnpJl1KBPcO._2q-ZKRaT1WjKg092R6La5J")
    for (let item of comment_button) {
    item.remove();
    }
    const in_comment_reply = document.querySelectorAll("._28lDeogZhLGXvE95QRPeDL")
    for (let item of in_comment_reply) {
    item.remove();
    }
    const gif_award = document.querySelectorAll("._15G4fCS1bzGgGK9kBOtN2t._28x1bnTjOY6zWZfooCxkKQ")
    for (let item of gif_award) {
    item.remove();
    }
    var header = document.getElementsByTagName('header')[0];
    header?.remove();
}
removeGradient()
