import axios from "./http"
const user={
    signin(params){
        return axios.post('/login',params)
    },
    getcase(data){
        return axios.get('/testcase_get',{params:data})
    },
    doubleballs(data){
        return axios.get('/double_balls',{params:data})
    },
    postcase(data){
        return axios.post('/testcase_store',data)
    }
}
export default user