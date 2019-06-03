<template>
    <div id="login">
        <div class="loginbox">
            <div class="logo">
                <img src="https://zj-live.max-digital.cn/storage/image/logo.png" alt="">
            </div>
            <Form :label-width="80">
                <FormItem label="账号">
                    <Input v-model="username" placeholder="请输入账号"></Input>
                </FormItem>
                <FormItem label="密码">
                    <Input v-model="password" placeholder="请输入密码"  type="password"></Input>
                </FormItem>
                <div style="text-align:center">
                    <Button class="zhijian-new-btn" type="primary" @click="handleSubmit()">登陆</Button>
                </div>
            </Form>
        </div>
    </div>
</template>
<script>
export default {
    name:"login",
    data(){
        return{
            username: '',
            password:''
        }
    },
    methods: {
        handleSubmit () {
            if(this.password === ''&& this.username===''){
                this.$Modal.error({
                    title:'提示',
                    content: '账号或者密码不为空'
                })
            }else{
                this.$http.post(this.PATH.LOGIN, {
                        username: this.username,
                        password: this.password
                    }).then(
                    success => {
                        console.log(success)
                        if(success.data.errno == '0') {
                            sessionStorage.setItem('username', success.data.data.username)
                            this.$router.push('/ActivityList');
                        }else {
                            this.loginFailed = false;
                            this.$Modal.error({
                                title:'提示',
                                content: success.data.errmsg,
                                onOk:()=>{
                                    
                                }
                            })
                        }
                    },
                    error => {
                    
                    }
                );
            }
            
        }
    }
}
</script>
<style lang="scss">
#login{
    position: absolute;
    width: 100%;
    height:100%;
    background:#ffc639;
    background-position: center;
    .loginbox{
        width: 500px;
        height: 350px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        -webkit-transform: translate(-50%, -50%);
        -moz-transform: translate(-50%, -50%);
        background-color: #fff;
        padding: 20px;
        box-sizing: border-box;
        -webkit-box-sizing: border-box;
        .logo{
            text-align: center;
            margin:20px 0px;
        }
    }
}
</style>
