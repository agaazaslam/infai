import type { Message } from "../App";

interface ChatBubbleProp {
  message: Message;
}

const ChatBubble: React.FC<ChatBubbleProp> = ({ message }) => {
  return (


    <div className={`chat   ${message.role === "user" ? "chat-end" : "chat-start"}`}>

      <div className="chat-header">
        {message.role == "assistant" ? "Query Agent " : "User"}
        <time className="text-xs opacity-50">{message.time}</time>
      </div>
      <div className={message.role == "assistant" ? "chat-bubble chat-bubble-neutral" : "chat-bubble chat-bubble-neutral"}>
        {message.message}
      </div>
    </div >




  )
}

export default ChatBubble
