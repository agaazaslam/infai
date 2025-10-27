
import { FileText, Github, Linkedin } from "lucide-react";
const Footer = () => {

  return (

    <footer className="bg-neutral p-3 flex justify-center items-center ">

      <div className="flex gap-3">
        <a href="https://github.com/agaazaslam/db-query" target="_blank" rel="noopener noreferrer" >
          <button className="btn btn-circle "> <Github /> </button>
        </a>

        <a href="https://www.linkedin.com/in/agaaz-aslam-00b960198/" target="_blank" rel="noopener noreferrer" >
          <button className="btn btn-circle "> <Linkedin /> </button>
        </a>



        <a href="https://drive.google.com/drive/folders/17Fi__Vn3uejZXN9C8_GX3zUaXXnEOAhv?usp=sharing" target="_blank" rel="noopener noreferrer" >
          <button className="btn btn-circle "> <FileText /> </button>
        </a>
      </div>

    </footer >


  )
}

export default Footer
