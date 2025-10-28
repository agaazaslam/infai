import { NewspaperIcon } from "lucide-react"
import { Link } from "react-router"

const Header = () => {
  return (

    <nav className="flex justify-between items-center p-3 bg-neutral text-neutral-content">
      <div className="container flex justify-between items-center mx-auto py-1 px-4 md:px-6 lg:px-8 ">

        <Link to={"/"}>        <div className="flex justify-center items-center gap-3">
          <div className="flex justify-center items-center bg-neutral-content w-8 h-8 md:w-12 md:h-12 rounded-xl">
            <NewspaperIcon className="text-neutral bg-neutral-content w-5 h-5 md:w-8 md:h-8 " />
          </div>
          <div className="text-neutral-content font-bold flex flex-col">
            <p className="text-md md:text-xl font-bold">Inf AI</p>
            <p className=" hidden md:block text-sm font-medium ">Powering News with AI </p>
          </div>
        </div>
        </Link>


        <div className=" flex justify-center items-center font-medium gap-2">

          <Link to={"/"}> Home </Link>
          <Link to={"/chat"}> Chat </Link>

        </div>

      </div>

    </nav>


  )
}

export default Header
