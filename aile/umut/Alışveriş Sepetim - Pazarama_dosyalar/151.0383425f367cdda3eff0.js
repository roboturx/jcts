(window.webpackJsonp=window.webpackJsonp||[]).push([[151],{1796:function(t,e,n){"use strict";n.r(e);var r={props:{categoryInfoTitle:{type:String,default:""},categoryLevel:{type:String,default:""},categoryId:{type:String,default:""}},head:function(){var t,e,n=this.$route.query.q,r=null!==(t=this.$route)&&void 0!==t&&null!==(e=t.query)&&void 0!==e&&e.sayfa?" - Sayfa ".concat(this.$route.query.sayfa):"",o=this.$route.params.slug?"".concat(this.$route.params.listing+" "+this.categoryInfoTitle):this.categoryInfoTitle;return n?{title:n+" - "+this.$config.CAPITALIZED_SITE_URL,meta:[{hid:"description",name:"description",content:n+" arama sonuç sayfasında aradığınız ürünü kolayca bulabilir, hızlı ve kolay bir şekilde satın alabilirsiniz."}]}:{title:o+" Ürünleri, Modelleri ve Fiyatları - "+this.$config.CAPITALIZED_SITE_NAME+r,meta:[{hid:"description",name:"description",content:o+" ürünleri, "+o+" fiyatları, "+o+" modelleri "+this.$config.CAPITALIZED_SITE_NAME+"'da! Tıkla, "+o+" ürünleri satın al."+r}]}},mounted:function(){this.$pushDataLayer({event:"category_view",categoryid:this.categoryId,level:this.categoryLevel})}},o=n(8),component=Object(o.a)(r,(function(){var t=this,e=t._self._c;return e("div",[t._t("bread-crumb"),t._v(" "),e("BaseContainer",[e("div",{staticClass:"flex"},[t._t("filter-left"),t._v(" "),e("div",{staticClass:"flex-1 pl-6.25 mb-9"},[t._t("filter-row"),t._v(" "),t._t("load-more-top"),t._v(" "),t._t("product-list"),t._v(" "),t._t("infinite-bottom"),t._v(" "),t._t("load-more-bottom"),t._v(" "),t._t("seo-content")],2)],2)])],2)}),[],!1,null,null,null);e.default=component.exports;installComponents(component,{BaseContainer:n(87).default})}}]);