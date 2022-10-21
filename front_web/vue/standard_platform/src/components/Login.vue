<template>
  <v-app>
    <v-content>
      <v-container py-5>
        <v-layout align-center justify-center py-3>
          <v-flex xs12 sm8 md4>
            <v-card class="px-2 pb-3">
              <v-card-text>
                <v-layout justify-center pt-2>
                  <v-avatar size="40px" color="pink">
                    <v-icon dark>Ziipin</v-icon>
                    <!-- <img src="https://vuetifyjs.com/apple-touch-icon-180x180.png" alt="avatar"> -->
                  </v-avatar>
                </v-layout>
                <v-layout justify-center py-3>
                  <div class="headline">Sign in</div>
                </v-layout>

                <v-form>
                  <v-text-field
                  
                    label="username"
                    type="text"
                    required
                    v-model="username"
                    :rules="accountRules"
                  ></v-text-field>
                  <v-text-field
                   
                  
                    label="Password"
                    type="password"
                    required
                    v-model="password"
                    :rules="passwordRules"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn block color="info" @click="submit">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
  


</template>

<script>
export default {
  name: "login",
  data() {
    return {
      username: "admin",
      accountRules: [
        v => !!v || "account is required",
        v => /.+@.+/.test(v) || "account must be valid"
      ],
      password: "123456",
      passwordRules: [v => !!v || "Password is required"]
    };
  },
  methods: {
    submit() {
        let post_data={
            "username":this.username,
            "password":this.password
        }
        this.$api.user.signin(post_data).then((result) => {
            console.log(result.data)
            if (result.data=="ok"){
              // this.$router.push({name:'main'})
              this.$router.push("/mainpage")  //$router跳转的两种方式
            }            
        }).catch((err) => {
            
        });
    }
  }
};
</script>