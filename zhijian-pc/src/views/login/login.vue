<template>
  <div id="login">
    <div class="login_content">
      <div class="main">
        <Row>
          <Col span="20" >
            <Row>
              <Col span="6" push="3">
                <Row type="flex" justify="center" align="middle" class="code-row-bg">
                  <Col span="24">
                    <div class="login_title">智见TV·后台</div>
                  </Col>
                  <Col span="24">
                    <Input prefix="ios-contact" @keyup.enter="handleSubmit" class="user_name" v-model="userName" placeholder="用户名" />
                  </Col>
                  <Col span="24">
                    <Input prefix="ios-contact2" @keyup.enter="handleSubmit" placeholder="密码" v-model="password" type="password" />
                  </Col>
                  <Col span="24">
                    <Button  class="login_btn" long @click="handleSubmit()" >登录</Button>
                  </Col>
                </Row>
              </Col>
            </Row>
          </Col>
        </Row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'login',
  data(){
    return {
      userName: '',
      password: ''
    }
  },
  created(){
     let that = this;
    document.onkeydown =function(e){
      e = window.event || e;
      if(e.code=='Enter'||e.code=='enter' || e.keyCode == 13){//验证在登录界面和按得键是回车键enter
        that.handleSubmit('login');//登录函数
      }
    }
   
  },
  methods: {
    handleSubmit () {
      if(this.userName === ''){
        this.$Modal.error({
          title: '提示',
          content: '用户名不为空'
        })
        return false;
      }
      if(this.password ===''){
        this.$Modal.error({
          title: '提示',
          content: '密码不为空'
        })
        return false;
      }
      this.$http.post(this.URL+this.PATH.LOGIN,{ user_name: this.userName, pass_word: this.password}).then(res=>{
        if(res.data.errno == 0){
            sessionStorage['userName'] = this.userName;
            this.$router.push('/classifyManagement');
            document.onkeydown = null;
        }else{
              this.$Modal.error({
                title: '提示',
                content: res.data.errmsg
            })
        }
      
      })
    },
  }
}
</script>

<style lang="less">
  html,body,#login{
    width: 100%;
    height: 100%;
  }
  .login_content{
    width: 100%;
    height: 100%;
    background: url("http://prjkmnaf0.bkt.clouddn.com/1558694453y8r3p0a9k0login_bg.png") no-repeat left top;
    background-size: 100% 100%;
    .main{
      width: 100%;
      height: 100%;
      padding: 98px 122px;
      >.ivu-row{
        width: 100%;
        height: 100%;
      }
      .ivu-col.ivu-col-span-20{
        width: 100%;
        height: 100%;
        background: url("http://prjkmnaf0.bkt.clouddn.com/1558694516z7yq8r2ac3login_main_bg.png") no-repeat left top;
        background-size: 100% 100%;
        .ivu-row{
          height: 100%;
          .ivu-col.ivu-col-span-6.ivu-col-push-3{
            position: relative;
            top: 50%;
            transform: translateY(-50%);
            .login_title{
              font-size: 32px;
              line-height: 45px;
              color: #333333;
              margin-bottom: 62px;
            }
            .ivu-input-with-prefix{
              height: 40px;
              border-radius: 5px;
              font-size: 21px;
              padding-top: 22px;
              padding-bottom: 22px;
              padding-left: 46px;
              color: #999999;
            }
            .ivu-col.ivu-col-span-24:nth-child(2){
              margin-bottom: 25px;
            }
            .ivu-col.ivu-col-span-24:nth-child(3){
              margin-bottom: 36px;
            }
            .ivu-icon{
              width: 27px;
              height: 29px;
              background: url("../../assets/img/user_icon.png") no-repeat left top;
              background-size: 27px 29px;
              position: relative;
              top: 8px;
              left: 10px;
              &::before{
                content: '';
              }
              &.ivu-icon-ios-contact2{
                background: url("../../assets/img/password_icon.png") no-repeat left top;
                left: 11px;
              }
            }
            .login_btn{
              background-image: linear-gradient(90deg, #535AFF 0%, #747DFF 100%);
              box-shadow: 0 2px 5px 0 #545AFF;
              border-color: transparent;
              font-size: 26px;
              color: #fff;
              border-radius: 0;
            }
          }
        }
      }
    }
  }
</style>
