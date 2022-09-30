import axios from "./http"
const user={
    signin(params){
        return axios.post('/login',params)
    },
    initial_all_case(){
        return axios.get('/testcase_get?id=0')
    }
 
}
export default user