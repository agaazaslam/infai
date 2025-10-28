import { Link } from "react-router"
import Footer from "../components/Footer"
import Header from "../components/Header"

const NotFound = () => {
  return (

    <div className="min-h-screen flex flex-col w-full text-neutral">
      <Header />
      <div className="flex flex-col grow p-4 gap-8 justify-center items-center  ">

        <h1 className="text-3xl font-medium"> Page Not Found </h1>
        <Link to={"/"}>

          <button className="btn btn-error"> Go to Home Page  </button>

        </Link>




      </div>

      <Footer />






    </div>
  )
}

export default NotFound
