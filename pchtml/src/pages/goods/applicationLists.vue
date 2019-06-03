<template>
  <div id="applicationLists">
    <div class="h1">下单名单</div>
    <div class="header">
      <Button class="newbtn zhijian-new-btn" @click="refresh" type="primary">刷新</Button>
    </div>
    <Table :data="allData" :columns="allColumns" stripe></Table>
    <div style="margin: 10px;overflow: hidden">
      <div style="float: right;">
        <Page :total="total" :current="page" @on-change="changePage"></Page>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "applicationLists",
  data() {
    return {
      goodsid: 1,
      page: 1,
      pagesize: 10,
      total: 50,
      allColumns: [
        {
          title: "序号",
          key: "num",
          width: 100
        },
        {
          title: "头像",
          key: "avatar_url",
          align: "center",
          render: (h, params) => {
            return h("img", {
              attrs: {
                src: params.row.avatar_url
              },
              style: {
                width: "60px",
                height: "60px",
                border: "1px solid",
                verticalAlign: "middle",
                margin: "10px"
              }
            });
          }
        },
        {
          title: "昵称",
          key: "nick_name",
          align: "center"
        },
        // {
        //   title: "助力值",
        //   key: "usr_zhuli_num",
        //   align: "center"
        // },
        // {
        //   title: "是否兑换",
        //   key: "is_change",
        //   align: "center",
        //   render: (h, params) => {
        //     return h("span", {}, params.row.is_change == 0 ? "否" : "是");
        //   }
        // },
        {
          title: "下单时间",
          key: "create_time",
          width: 200,
          align: "center"
        }
      ],
      allData: []
    };
  },
  created() {
    const routeParams = this.$route.params;
    this.goodsid = routeParams.goodsid;
    this.getData();
  },

  methods: {
    getData() {
      this.$http
        .post(this.PATH.GOODSUSERINFO, {
          goods_id: this.goodsid,
          page: this.page,
          pagesize: this.pagesize
        })
        .then(res => {
          console.log(res);
          if (res.data.errno === 0) {
            this.allData = res.data.data;
            this.total = res.data.count;
          }
        });
    },
    /**
     * 分页
     */
    changePage(page) {
      this.page = page;
      this.getData();
    },
    refresh() {
      this.getData();
    }
  }
};
</script>
<style lang="scss">
#applicationLists {
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  .h1 {
    font-size: 22px;
    color: #808080;
  }
  .header {
    margin-top: 20px;
    text-align: right;
    margin-bottom: 30px;
    position: relative;
    height: 42px;
    //新增按钮
    .newbtn {
      float: right;
      text-align: left;
      margin-left: 10px;
    }
    &:before,
    &:after {
      display: table;
      line-height: 0;
      content: "";
    }
    &:after {
      clear: both;
    }
  }
}
</style>
