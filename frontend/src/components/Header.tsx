import { NewspaperIcon } from "lucide-react"
import { Link } from "react-router"

const Header = () => {
  return (

    <nav className="flex justify-between items-center p-3 bg-neutral text-neutral-content">
      <div className="container flex justify-between items-center mx-auto py-1 px-8 ">

        <div className="flex justify-center items-center gap-3">
          <div className="flex justify-center items-center bg-neutral-content w-11 h-11 rounded-xl">
            <NewspaperIcon className="text-neutral bg-neutral-content w-8 h-8" />
          </div>
          <div className="text-neutral-content font-bold flex flex-col">
            <p className="text-xl font-bold">Inf AI</p>
            <p className="text-sm font-medium ">Powering News with AI </p>


          </div>
        </div>

        <div className=" flex justify-center items-center font-medium gap-2">

          <Link to={"/"}> Home </Link>
          <Link to={"/chat"}> Chat </Link>

        </div>

      </div>

    </nav>


  )
}

export default Header
