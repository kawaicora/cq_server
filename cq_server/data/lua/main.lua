
local common_utils = require('common_utils')
function main()
    common_utils.init()

    ScriptLib.PrintContextLog(common_utils, "LUA_INFO : main!")
    local chat_id = ScriptLib.TelegramBotGetChatId()
    ScriptLib.TelegramBotSendMessage(chat_id,"LUA_INFO : main!")
    
end

main()