<template>
<div id='home'>
  <div class="layout">
    <div class="container_header ">
        <div class="company-name">智见TV</div>
        <div class='signOut' @click="signOut">退出登录</div>
         <div class="userName">{{userName}}</div>
    </div>
     <Layout breakpoint="lg">
        <Sider hide-trigger collapsible :collapsed-width="0">
          <Menu
            @on-select="routeTo"
            width="auto"
            accordion
            active-name="2"
          >
            <MenuItem name="1">
              <!--<Icon type="md-document"></Icon>-->
              <Icon custom="i-icon view_icon" />
              <span>概览</span>
            </MenuItem>
            <MenuItem name="2">
              <Icon custom="i-icon classify_icon" />
              <span>分类管理</span>
            </MenuItem>
            <MenuItem name="3">
              <Icon custom="i-icon chosen_icon" />
              <span>精选管理</span>
            </MenuItem>
            <MenuItem name="4">
              <Icon custom="i-icon upload_icon" />
              <span>上传视频</span>
            </MenuItem>
          </Menu>
        </Sider>
        <Layout>
          <router-view/>
        </Layout>
    </Layout>
      <div class="modal">
        <Modal
          v-model="modal.modalClick"
          title="提示"
          @on-ok="asyncOK(modal.modalType)"
          >
          <p>{{modal.txtInfo}}</p>
        </Modal>
      </div>
  </div>

      
   
</div>
</template>
<script>
import routers from "@/router/routePath"
export default {
  name: 'home',
  components: {
  },
  data(){
    return {
      routes: routers.routes,
      userName: sessionStorage['userName'],
      activeName: "2",
      openNames: ["2"],
      // 退出登录参数
        modal: {
        modalClick: false,
        modalType:'signOut',
        txtInfo: '确定退出登录吗？',
      }
    }
  },
  methods:{
    routeTo(name) {
      switch (name) {
        case "1":
        this.modal.txtInfo = '开发中,敬请期待';
        this.modal.modalType = 1;
        this.modal.modalClick = true;
          break;
        case "2":
          this.$router.push({ name: "classifyManagement" });
          break;
        case "3":
        this.modal.txtInfo = '开发中,敬请期待';
        this.modal.modalType = 1;
        this.modal.modalClick = true;
          break;
        case "4":
          this.$router.push({ name: "uploadVideo" });
          break;
        default:
      }
    },
    // 退出登录
    signOut(){
      this.modal.modalClick = true;
      this.modal.txtInfo = '确定退出登录吗？'
      this.modal.modalType = 'signOut';
    },
    // 退出登录的确定
    asyncOK (from) {
      console.log(from)
      if( from == 'signOut'){
          sessionStorage.clear()
          this.$router.push({
          name:'login'
          })
      }
    },
  }
}
</script>
<style lang="less">
  @base: #6461FF;
  html,body,#home{
    height: 100%;
  }
  .container_header{
    width: 100%;
    height: 71px;
    line-height: 71px;
    background-image: linear-gradient(-130deg, #7E5FFF 0%, #525AFF 100%);
    .company-name{
      font-family: PingFangSC-Semibold;
      font-size: 24px;
      color: #FFFFFF;
      letter-spacing: 0;
      float: left;
      text-align: center;
      box-shadow: 1px 0 7px 0 rgba(67,67,67,0.50);
      width: 227px;
      }
    .userName{
      float: right;
      font-family: PingFangSC-Medium;
      font-size: 18px;
      color: #FFFFFF;
      letter-spacing: 0;
      text-align: justify;
      margin-right: 25px;
    }
  }
  .ivu-layout{
    height: 100%;
    .ivu-menu-vertical.ivu-menu-light:after{
      background: #fff;
    }
    .ivu-layout-sider{
      min-width:227px !important;
      max-width: 227px !important;
      box-shadow: 1px 12px 11px 1px #E0E1FF;
      background-color: #fff !important;
      .ivu-menu-item{
        height: 50px;
        line-height: 50px;
        color: #999;
        font-size: 14px;
        padding: 0;
        position: relative;
        span{
          display: inline-block;
          line-height: 50px;
        }
        .i-icon{
          width: 30px;
          height: 30px;
          position: absolute;
          left: 49px;
          top: 15px;
        }
        .view_icon{
          background: url("../assets/img/view_icon_default.png") no-repeat left top;
          background-size: 18px 18px;
        }
        .classify_icon{
          background: url("../assets/img/classify_icon_default.png") no-repeat left top;
          background-size: 18px 18px;
        }
        .chosen_icon{
          background: url("../assets/img/chosen_icon_default.png") no-repeat left top;
          background-size: 22px 20px;
          left: 47px;
        }
        .upload_icon{
          background: url("../assets/img/upload_icon_default.png") no-repeat left top;
          background-size: 22px 22px;
          left: 47px;
        }
        &:hover{
          color: @base;
          .view_icon{
            background: url("../assets/img/view_icon_hover.png") no-repeat left top;
          }
          .classify_icon{
            background: url("../assets/img/classify_icon_hover.png") no-repeat left top;
          }
          .chosen_icon{
            background: url("../assets/img/chosen_icon_hover.png") no-repeat left top;
          }
          .upload_icon{
            background: url("../assets/img/upload_icon_hover.png") no-repeat left top;
          }
        }
      }
      .ivu-menu-vertical .ivu-menu-submenu-title{
        padding: 0;
      }
      .ivu-menu-item.ivu-menu-item-active.ivu-menu-item-selected{
        background-image: linear-gradient(-222deg, #525CFF 0%, #8368FE 100%);
        color: #fff;
        .view_icon{
          background: url("../assets/img/view_icon_active.png") no-repeat left top;
        }
        .classify_icon{
          background: url("../assets/img/classify_icon_active.png") no-repeat left top;
        }
        .chosen_icon{
          background: url("../assets/img/chosen_icon_active.png") no-repeat left top;
        }
        .upload_icon{
          background: url("../assets/img/upload_icon_active.png") no-repeat left top;
        }
      }
      .ivu-menu-light.ivu-menu-vertical .ivu-menu-item-active:not(.ivu-menu-submenu):after{
        content: '';
        display: none;
        width: 0;
        position: absolute;
        top: 0;
        bottom: 0;
        right: 0;
        background: #8368FE;
      }

    }
    .ivu-layout{
      height: 100%;
      padding: 20px 65px 25px 44px;
      background: #F2F6F9;

    }
  }
// 统一修改弹窗的样式
.ivu-modal-wrap{
  .ivu-modal{
    width: 483px !important;
    height: 287px;
    top: 50%;
    margin-top: -143px;
    /*position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);*/
    .ivu-modal-content{
      .ivu-modal-header{
        padding-top: 16px;
        padding-left: 34px;
        position: relative;
        .ivu-modal-close{
          .ivu-icon-ios-close{
            font-size: 38px;
            top: -2px;
          }
        }
        .ivu-modal-header-inner{
          font-size: 18px;
          color: @base;
          &::after{
            content: '';
            display: inline-block;
            width: 59px;
            height: 2px;
            background: @base;
            position: absolute;
            bottom: -1px;
            left: 24px;
          }
        }
      }
      .ivu-modal-body{
        padding: 20px;
        >p{
          font-size: 18px;
          color: @base;
          text-align: center;
          &::before{
            content: '？';
            display: block;
            width: 40px;
            height: 40px;
            line-height: 40px;
            font-size: 33px;
            color: #fff;
            font-weight: bold;
            background: @base;
            border-radius: 50%;
            margin: 0 auto;
            margin-bottom: 14px;
            padding-left: 12px;
          }
        }
      }
      .ivu-modal-footer{
        text-align: center;
        border-top-color: transparent;
        padding-bottom: 40px;
        button{
          width: 71px;
          height: 35px;
          line-height: 16px;
          border-radius: 1.23px;
          font-size: 16px;
          &.ivu-btn-primary{
            background: @base;
            /*margin-left: 52px;*/
            border-color: transparent;
          }
          &.ivu-btn-text{
            background: #F2F2F2;
            border: 1px solid #E6E6E6;
            color: #999;
            display: none;
          }
        }
      }
    }
  }
}
  .layout{
    background: #f5f7f9;
    position: relative;
    overflow: hidden;
    height: 100%;
    padding-bottom: 70px;
  }
  .signOut{
    float: right;
    color: #fff;
    font-size: 18px;
    margin-right: 20px;
    cursor: pointer;
  }
</style>
<style>

</style>
