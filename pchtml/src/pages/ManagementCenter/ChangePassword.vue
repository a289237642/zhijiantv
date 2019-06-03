<template>
    <div id="ChangePassword">
        <div class="h1">修改密码</div>
        <div class="container">
            <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
                <FormItem label="原密码" prop="passwordo">
                    <Input v-model="formValidate.passwordo" placeholder="请输入原密码" type="password"></Input>
                </FormItem>
                <FormItem label="新密码" prop="password1">
                    <Input v-model="formValidate.password1" placeholder="请输入新密码" type="password"></Input>
                </FormItem>
                <FormItem label="确认密码" prop="password2">
                    <Input v-model="formValidate.password2" placeholder="请输入新密码" type="password"></Input>
                </FormItem>
                <FormItem>
                    <Button class="zhijian-new-btn" type="primary" @click="handleSubmit('formValidate')">提交</Button>
                </FormItem>
            </Form>
       </div>
    </div>
</template>
<script>
export default {
    name:"ChangePassword",
    data(){
        // 验证pass
        const validatePass = (rule, value, callback) => {
            if (value === "") {
                callback(new Error("请输入新密码"));
            }else {
                if (this.formValidate.password2 !== "") {
                // 对第二个密码框单独验证
                this.$refs.formValidate.validateField("password2");
                }
                callback();
            }
        };
        // 验证2次pass
        const validatePassCheck = (rule, value, callback) => {
            if (value === "") {
                callback(new Error("请再次输入新密码"));
            } else if (value !== this.formValidate.password1) {
                callback(new Error("两次输入密码不一致"));
            } else {
                callback();
            }
        };
        return{
            username:sessionStorage.getItem('username'),
            formValidate: {
                passwordo: '',
                password1: '',
                password2: ''
            },
            ruleValidate: {
                passwordo: [
                    { required: true, message: '请输入原密码', trigger: 'blur' }
                ],
                password1: [
                    { required: true, validator: validatePass, trigger: 'blur' }
                ],
                password2: [
                    { required: true, validator: validatePassCheck, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    if(this.formValidate.passwordo==this.formValidate.password1){
                        this.$Modal.error({
                            title:'提示',
                            content: '新密码与原密码相同，请重新输入'
                        });
                    }else{
                        this.$http.post(this.PATH.CHANGEPWD, {
                            username:this.username,
                            passwordo: this.formValidate.passwordo,
                            password1: this.formValidate.password1,
                            password2: this.formValidate.password2
                        }).then(
                            success => {
                                if(success.data.status == '0') {
                                    this.$Modal.error({
                                        title:'提示',
                                        content: success.data.msg,
                                        onOk:()=>{
                                            this.formValidate.passwordo='';
                                            this.formValidate.password1='';
                                            this.formValidate.password2='';
                                        }
                                    })
                                }else {
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
                    
                } else {
                    this.$Message.error(success.data.errmsg);
                }
            })
        },
    }
}
</script>
<style lang="scss">
#ChangePassword{
    height: 100%;
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    .h1{
        font-size: 22px;
        color: #808080;
    }
    .container{
        margin-top: 20px;
    }
}
</style>
