import { useState, type ChangeEvent } from "react";
import ChatBubble from "../components/ChatBubble";
import axios from "axios";
import { Ellipsis, Send } from "lucide-react";
import { startupMessage } from "../components/message";
import Footer from "../components/Footer.tsx";
import Header from "../components/Header.tsx";

export interface Message {
  time: string;
  message: string;
  role: string;
}


function Chat() {

  const startUp: Message = { time: "12PM", message: startupMessage, role: "assistant" }

  const [messages, setMessages] = useState<Message[]>([startUp]);
  const [input, setInput] = useState<string>("");
  const [isLoading, setisLoading] = useState<boolean>(false);

  const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";




  const handleSubmit = async () => {
    try {

      setisLoading(true);
      if (!input.trim()) return;
      const userMessage = { "time": "12PM", "message": input, "role": "user" }
      setMessages(prev => [...prev, userMessage]);
      setInput("");

      const response = await axios.post(`${apiUrl}/query`, userMessage);
      console.log(response.data);
      setMessages(prev => [...prev, response.data]);



    } catch (error) {
      console.log(error);

    }
    finally {
      setisLoading(false);
    }
  }

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  }

  return (
    <>

      <div className="w-full min-h-screen flex flex-col">
        <Header />

        <div className="flex flex-col flex-grow max-w-7xl mx-auto bg-neutral m-3 mb-10">

          {/* Chat messages area */}
          <div className="h-[80vh] bg-base-300 overflow-y-auto p-4 flex flex-col gap-2">
            {messages.map((msg) => (
              <ChatBubble message={msg} key={msg.message} />
            ))}

            {isLoading && (
              <div className="chat chat-start p-4 text-secondary-content font-semibold flex items-center gap-2">
                Thinking <Ellipsis className="text-black h-8 w-8 animate-pulse" />
              </div>
            )}
          </div>

          {/* Input area */}
          <div className="flex items-center gap-2  p-2">
            <input
              type="text"
              value={input}
              onChange={handleInput}
              placeholder="Type here"
              className="input flex-grow"
            />
            <button className="btn btn-soft" onClick={handleSubmit}>

              <Send />
            </button>
          </div>

        </div>

        <Footer />
      </div>
    </>
  )
}

export default Chat
