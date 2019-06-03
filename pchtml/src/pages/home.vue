<template>
  <div id="home">
    <div class="layout">
      <div class="container_head">
        <div>
          <img src="@/assets/images/logo.png" alt="LOGO">
          <div>
            <div>
              {{username}}
              <Icon type="md-arrow-dropdown"/>
              <section class="nav_section_list">
                <ul>
                  <li @click="loginout">
                    <span>登出</span>
                  </li>
                </ul>
              </section>
            </div>
          </div>
        </div>
      </div>
      <Layout breakpoint="lg">
        <Sider ref="side1" hide-trigger collapsible :collapsed-width="0">
          <Menu
            @on-select="routeTo"
            :active-name="activeName"
            :open-names="openNames"
            theme="dark"
            width="auto"
            accordion
          >
            <!-- <template slot="title">
                            <Icon class="iconfont icon-pinpai"></Icon>
                            <span></span>
            </template>-->
            <!-- <MenuItem name="1-1">
                      <Icon class="iconfont icon-shouye2"></Icon>
                        <span>首页</span>
            </MenuItem>-->
            <Submenu name="2">
              <template slot="title">
                <Icon class="iconfont icon-chanpinguanli"></Icon>
                <span>活动管理</span>
              </template>
              <MenuItem name="2-1">
                <span>活动列表</span>
              </MenuItem>
            </Submenu>
            <Submenu name="3">
              <template slot="title">
                <Icon class="iconfont icon-dingdanguanli"></Icon>
                <span>爆料管理</span>
              </template>
              <MenuItem name="3-1">
                <span>爆料列表</span>
              </MenuItem>
              <MenuItem name="3-11">
                <span>文章标签管理</span>
              </MenuItem>
              <MenuItem name="3-12">
                <span>文章敏感词管理</span>
              </MenuItem>
              <MenuItem name="3-7">
                <span>icon管理</span>
              </MenuItem>
              <MenuItem name="3-8">
                <span>签到海报管理</span>
              </MenuItem>
              <MenuItem name="3-2">
                <span>24小时热榜</span>
              </MenuItem>
              <MenuItem name="3-3">
                <span>爆料库</span>
              </MenuItem>
              <MenuItem name="3-4">
                <span>爆料类型管理</span>
              </MenuItem>
              <MenuItem name="3-5">
                <span>Banner管理</span>
              </MenuItem>
              <MenuItem name="3-6">
                <span>学堂管理</span>
              </MenuItem>
              <MenuItem name="3-9">
                <span>公众号库</span>
              </MenuItem>
              <MenuItem name="3-10">
                <span>公众号列表</span>
              </MenuItem>
            </Submenu>
            <Submenu name="7">
              <template slot="title">
                <Icon class="iconfont icon-dingdanguanli"></Icon>
                <span>认知</span>
              </template>
              <MenuItem name="7-1">
                <span>今日免费听</span>
              </MenuItem>
              <MenuItem name="7-2">
                <span>商学院</span>
              </MenuItem>
              <MenuItem name="7-3">
                <span>课程类型管理</span>
              </MenuItem>
            </Submenu>
            <Submenu name="8">
              <template slot="title">
                <Icon class="iconfont icon-chanpinguanli"></Icon>
                <span>商品管理</span>
              </template>
              <MenuItem name="8-1">
                <span>商品列表</span>
              </MenuItem>
            </Submenu>
            <Submenu name="10">
              <template slot="title">
                <Icon class="iconfont icon-dingdanguanli"></Icon>
                <span>订单管理</span>
              </template>
              <MenuItem name="10-1">
                <span>订单列表</span>
              </MenuItem>
            </Submenu>
            <Submenu name="9">
              <template slot="title">
                <Icon class="iconfont icon-chanpinguanli"></Icon>
                <span>换量管理</span>
              </template>
              <MenuItem name="9-1">
                <span>换量列表</span>
              </MenuItem>
            </Submenu>
            <Submenu name="11">
              <template slot="title">
                <Icon class="iconfont icon-chanpinguanli"></Icon>
                <span>渠道管理</span>
              </template>
              <MenuItem name="11-1">
                <span>渠道列表</span>
              </MenuItem>
              <MenuItem name="11-2">
                <span>数据概览</span>
              </MenuItem>
            </Submenu>
            <Submenu name="6">
              <template slot="title">
                <Icon class="iconfont icon-shouye2"></Icon>
                <span>课程管理</span>
              </template>
              <MenuItem name="6-1">
                <span>课程列表</span>
              </MenuItem>
              <MenuItem name="6-4">
                <span>课程库</span>
              </MenuItem>
              <MenuItem name="6-3">
                <span>头像库</span>
              </MenuItem>
            </Submenu>
            <Submenu name="4">
              <template slot="title">
                <Icon class="iconfont icon-yonghuguanli"></Icon>
                <span>用户管理</span>
              </template>
              <MenuItem name="4-1">
                <span>用户列表</span>
              </MenuItem>
            </Submenu>
            <Submenu name="5">
              <template slot="title">
                <Icon class="iconfont icon-zhanghuguanli"></Icon>
                <span>管理中心</span>
              </template>
              <MenuItem name="5-1">
                <span>更改密码</span>
              </MenuItem>
            </Submenu>
          </Menu>
        </Sider>
        <Layout>
          <Content :style="{padding:0, background: '#eeeeee'}">
            <router-view/>
          </Content>
        </Layout>
      </Layout>
    </div>
  </div>
</template>
<script>
import routers from "@/router/routePath";
export default {
  name: "home",
  data() {
    return {
      routes: routers.routes,
      username: sessionStorage.getItem("username"),
      activeName: "2-1",
      openNames: ["2"]
    };
  },
  computed: {},
  created() {
    this.setNav();
  },
  watch: {
    $route: "setNav"
  },
  methods: {
    loginout() {
      this.$http.get(this.PATH.LOGINOUT).then(res => {
        console.log(res);
      });
      sessionStorage.removeItem("username");
      this.$router.push({ name: "login" });
    },
    routeTo(name) {
      switch (name) {
        case "1-1":
          this.$router.push({ name: "index" });
          break;
        case "2-1":
          this.$router.push({ name: "ActivityList" });
          break;
        case "3-1":
          this.$router.push({ name: "tipoffList" });
          break;
        case "3-2":
          this.$router.push({ name: "CompanyHeadline" });
          break;
        case "3-3":
          this.$router.push({ name: "tipoffLibrary" });
          break;
        case "3-4":
          this.$router.push({ name: "tipoffManagement" });
          break;
        case "3-5":
          this.$router.push({ name: "bannerManagement" });
          break;
        case "3-6":
          this.$router.push({ name: "schoolManagement" });
          break;
        case "3-7":
          this.$router.push({ name: "iconManagement" });
          break;
        case "3-8":
          this.$router.push({ name: "signManagement" });
          break;
        case "3-9":
          this.$router.push({ name: "vipcnLibrary" });
          break;
        case "3-10":
          this.$router.push({ name: "vipcnList" });
          break;
        case "3-11":
          this.$router.push({ name: "keywordsManagement" });
          break;
        case "3-12":
          this.$router.push({ name: "sensitivewordsManagement" });
          break;
        case "4-1":
          this.$router.push({ name: "userList" });
          break;
        case "5-1":
          this.$router.push({ name: "ChangePassword" });
          break;
        case "6-1":
          this.$router.push({ name: "lessonManagement" });
          break;
        case "6-3":
          this.$router.push({ name: "headImage" });
          break;
        case "6-4":
          this.$router.push({ name: "lessonLibray" });
          break;
        case "7-1":
          this.$router.push({ name: "freeListen" });
          break;
        case "7-2":
          this.$router.push({ name: "business" });
          break;
        case "7-3":
          this.$router.push({ name: "typeManagement" });
          break;
        case "8-1":
          this.$router.push({ name: "goodsList" });
          break;
        case "9-1":
          this.$router.push({ name: "advList" });
          break;
        case "11-1":
          this.$router.push({ name: "channelList" });
          break;
        case "11-2":
          this.$router.push({ name: "dataOverview" });
          break;
        case "10-1":
          this.$router.push({ name: "orderList" });
          break;
        // case "6-2":
        //   this.$router.push({ name: "lessonAudio" })
        //   break
        default:
      }
    },
    //设置菜单高亮
    setNav() {
      let routeName = this.$route.name;
      // console.log(
      //   this.routes,
      //   this.$route.name,
      //   this.routes[routeName],
      //   "route"
      // );
      this.activeName = this.routes[routeName].id;
      this.openNames = this.routes[routeName].parent;
      /*this.$nextTick(function () {
          this.$refs.Menu.updateOpened()
          this.$refs.Menu.updateActiveName()
        })*/
    }
  }
};
</script>
<style lang="scss">
#home {
  height: 100%;
  .ivu-menu-dark.ivu-menu-vertical .ivu-menu-opened .ivu-menu-submenu-title {
    background: #272b2f;
    /*color: var(--base);*/
  }
  .ivu-menu-dark.ivu-menu-vertical
    .ivu-menu-child-item-active
    > .ivu-menu-submenu-title {
    color: var(--base);
  }
  .menu-item .iconfont {
    position: relative;
    top: -6px;
  }
}

.container_head {
  width: 100%;
  height: 60px;
  background-color: #1c2428;
  > div {
    position: relative;
    height: 100%;
    > img {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 40px;
      margin-left: 50px;
    }
    > i {
      margin: 18px 20px 0 20px;
    }
    .ivu-icon-md-menu:before {
      color: var(--base);
    }
    > div {
      float: right;
      color: #fff;
      position: relative;
      font-size: 14px;
      line-height: 60px;
      // margin-right: 40px;
      cursor: pointer;
      height: 90px;
      &:hover {
        .nav_section_list {
          display: block;
        }
      }
    }
    .nav_section_list {
      display: none;
      z-index: 999;
      position: absolute;
      background-color: #ffffff;
      top: 45px;
      right: -3px;
      /*box-shadow: 4px 5px 10px 0 #e5e5e5;*/
      transition: all 0.2s linear;
      // border-radius: 4px;
      &:hover {
        background-color: var(--base);
        background-color: #ffc639;
      }
      ul {
        list-style: none;
        li {
          width: 80px;
          text-align: center;
          height: 30px;
          color: #000;
          cursor: pointer;
          font-size: 12px;
          line-height: 30px;
        }
      }
    }
  }
}
.ivu-layout-sider {
  background: #272b2f !important;
}
.ivu-layout.ivu-layout-has-sider {
  height: 100%;
}
.ivu-layout-sider {
  overflow: auto;
}
.ivu-menu-dark {
  background: #272b2f;
  padding: 10px 0 100px 0;
}
.ivu-menu-dark.ivu-menu-vertical .ivu-menu-item-active:not(.ivu-menu-submenu),
.ivu-menu-dark.ivu-menu-vertical
  .ivu-menu-submenu-title-active:not(.ivu-menu-submenu) {
  color: var(--base) !important;
}
.ivu-menu-dark.ivu-menu-vertical .ivu-menu-item-active:not(.ivu-menu-submenu),
.ivu-menu-dark.ivu-menu-vertical
  .ivu-menu-item-active:not(.ivu-menu-submenu):hover,
.ivu-menu-dark.ivu-menu-vertical
  .ivu-menu-submenu-title-active:not(.ivu-menu-submenu),
.ivu-menu-dark.ivu-menu-vertical
  .ivu-menu-submenu-title-active:not(.ivu-menu-submenu):hover {
  background: #272b2f !important;
}
.ivu-menu-dark.ivu-menu-vertical .ivu-menu-item,
.ivu-menu-dark.ivu-menu-vertical .ivu-menu-submenu-title {
  background: #272b2f !important;
}
.ivu-menu-dark.ivu-menu-vertical .ivu-menu-submenu .ivu-menu-item-active,
.ivu-menu-dark.ivu-menu-vertical .ivu-menu-submenu .ivu-menu-item-active:hover {
  border-right: none;
  color: var(--base) !important;
  background: #272b2f !important;
}
.ivu-menu-submenu {
  white-space: nowrap;
}
.layout {
  background: #f5f7f9;
  position: relative;
  overflow: hidden;
  height: 100%;
}
.layout-header-bar {
  background: #fff;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
}
.layout-logo-left {
  width: 90%;
  height: 30px;
  background: #5b6270;
  border-radius: 3px;
  margin: 15px auto;
}
.menu-icon {
  transition: all 0.3s;
}
.rotate-icon {
  transform: rotate(-90deg);
}
.menu-item span {
  display: inline-block;
  overflow: hidden;
  /*width: 69px;*/
  /*text-overflow: ellipsis;*/
  /*white-space: nowrap;*/
  /*vertical-align: bottom;*/
  transition: width 0.2s ease 0.2s;
}
.menu-item i {
  transform: translateX(0px);
  transition: font-size 0.2s ease, transform 0.2s ease;
  vertical-align: middle;
  font-size: 16px;
}
.collapsed-menu span {
  width: 0px;
  transition: width 0.2s ease;
}
.collapsed-menu i {
  transform: translateX(5px);
  transition: font-size 0.2s ease 0.2s, transform 0.2s ease 0.2s;
  vertical-align: middle;
  font-size: 22px;
}
</style>


