import axios from "./http"
const user={
    signin(params){
        return axios.post('/login',params)
    }
}
export default user