import { useState, type ChangeEvent } from "react";
import ChatBubble from "./components/ChatBubble";
import axios from "axios";
import { Database, Ellipsis, FileText, Github, Linkedin, Newspaper, Send } from "lucide-react";
import { startupMessage } from "./components/message";
import Footer from "./components/Footer";

export interface Message {
  time: string;
  message: string;
  role: string;
}


function App() {

  const startUp: Message = { time: "12PM", message: startupMessage, role: "assistant" }
  const startUp2: Message = { time: "12PM", message: startupMessage, role: "user" }

  const [messages, setMessages] = useState<Message[]>([startUp, startUp2]);
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
        <nav className="bg-neutral p-2 text-white flex justify-between  ">

          <div className="font-bold flex gap-2 text-white text-2xl items-center"> <Newspaper /> InfAI  </div>
        </nav>

        <div className="flex-col flex-grow  mx-auto  m-3 bg-primary mb-10" >

          <div className="w-full md:min-w-xl container h-[83vh] bg-base-300 overflow-y-auto p-4 ">





            {messages.map((msg) => <ChatBubble message={msg} key={msg.message} />)}

            {isLoading && <div className="chat chat-start p-4 text-secondary-content font-semibold "> Thinking  <Ellipsis className=" text-black h-8 w-8 animate-pulse " /> </div>}


          </div>
          <div className="flex justify-center items-center m-2 gap-1 ">

            <input type="text" value={input} onChange={handleInput} placeholder="Type here" className="input w-full " />
            <button className="btn btn-soft" onClick={handleSubmit}> <Send /> </button>

          </div>
        </div>
        <Footer />

      </div >
    </>
  )
}

export default App
