(window.webpackJsonp=window.webpackJsonp||[]).push([[10,72,75,87,144],{1199:function(e,t,n){var content=n(1220);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(36).default)("68e1f727",content,!0,{sourceMap:!1})},1211:function(e,t,n){e.exports=n.p+"img/bcc81dd.png"},1213:function(e,t,n){var content=n(1245);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(36).default)("37e22d33",content,!0,{sourceMap:!1})},1218:function(e,t,n){n(23)({target:"Math",stat:!0},{trunc:n(567)})},1219:function(e,t,n){"use strict";n(1199)},1220:function(e,t,n){var r=n(35)((function(i){return i[1]}));r.push([e.i,'.countdown[data-v-65c9a98c]{display:flex;justify-content:flex-end}.countdown .countdown__block[data-v-65c9a98c]{padding:0 .3125rem;position:relative;text-align:center}.countdown .countdown__block[data-v-65c9a98c]:first-child{padding-left:0}.countdown .countdown__block:first-child .countdown__day[data-v-65c9a98c]:before,.countdown .countdown__block:first-child .countdown__digit[data-v-65c9a98c]:before{display:none}.countdown .countdown__block[data-v-65c9a98c]:last-child{padding-right:0}.countdown .countdown__digit[data-v-65c9a98c]{font-weight:700;line-height:1}.countdown .countdown__digit[data-v-65c9a98c]:before{--tw-content:":";content:":";content:var(--tw-content);left:-.3125rem;position:absolute}.countdown .countdown__day[data-v-65c9a98c]{font-weight:700;line-height:1}.countdown .countdown__day[data-v-65c9a98c]:before{left:-.3125rem;position:absolute}',""]),r.locals={},e.exports=r},1227:function(e,t,n){"use strict";n.r(t);n(11),n(64),n(1218),n(156),n(92);var r={filters:{twoDigits:function(e){return e.toString().length<=1?"0"+e.toString():e.toString()}},props:{date:{type:String,default:""},customClass:{type:[String,Array,Object],default:null},color:{type:String,default:""},isCustomSlot:{type:Boolean,default:!0},isTimerButton:{type:Boolean,default:!1}},data:function(){return{now:Math.trunc((new Date).getTime()/1e3),event:null,finish:!1}},computed:{secondCount:function(){return this.calculatedDate-this.now},calculatedDate:function(){return Math.trunc(Date.parse(this.event)/1e3)},seconds:function(){return this.secondCount<0?0:this.secondCount%60},minutes:function(){return this.secondCount<0?0:Math.trunc(this.secondCount/60)%60},hours:function(){return this.secondCount<0?0:Math.trunc(this.secondCount/60/60)%24},days:function(){return this.secondCount<0?0:Math.trunc(this.secondCount/60/60/24)},classObject:function(){return Object.values({color:this.color,customClass:this.customClass})},isLastTenMinutes:function(){return 0===this.days&&0===this.hours&&this.minutes<10}},watch:{date:{handler:function(e){this.event=e},immediate:!0}},mounted:function(){var e=this,t=this,time=setInterval((function(){e.now=Math.trunc((new Date).getTime()/1e3),!e.finish&&e.calculatedDate-e.now<=0&&(t.finish=!0,t.$emit("onFinish"),clearInterval(time))}),1e3)}},o=(n(1219),n(8)),component=Object(o.a)(r,(function(){var e=this,t=e._self._c;return t("div",{staticClass:"flex justify-end items-baseline pr-2.5",class:e.classObject},[e.isCustomSlot?e._t("default",null,{days:e._f("twoDigits")(e.days),hours:e._f("twoDigits")(e.hours),minutes:e._f("twoDigits")(e.minutes),seconds:e._f("twoDigits")(e.seconds),isLastTenMinutes:e.isLastTenMinutes}):[e.isTimerButton?e._e():t("span",{staticClass:"mr-2 text-xs leading-none"},[e._v("Kalan Süre: ")]),e._v(" "),t("div",{staticClass:"countdown"},[e.days?t("div",{class:["countdown__block",{"!pr-0":e.isTimerButton}]},[t("div",{staticClass:"countdown__digit"},[e._v("\n          "+e._s(e._f("twoDigits")(e.days))+e._s(e.isTimerButton?":":"Gün")+"\n        ")])]):e._e(),e._v(" "),t("div",{class:["countdown__block",{"!pl-px":e.isTimerButton}]},[t("div",{staticClass:"countdown__day"},[e._v("\n          "+e._s(e._f("twoDigits")(e.hours))+"\n        ")])]),e._v(" "),t("div",{class:["countdown__block",{"!pl-px":e.isTimerButton}]},[t("div",{staticClass:"countdown__digit"},[e._v("\n          "+e._s(e._f("twoDigits")(e.minutes))+"\n        ")])]),e._v(" "),t("div",{class:["countdown__block",{"!pl-px":e.isTimerButton}]},[t("div",{staticClass:"countdown__digit"},[e._v("\n          "+e._s(e._f("twoDigits")(e.seconds))+"\n        ")])])])]],2)}),[],!1,null,"65c9a98c",null);t.default=component.exports},1244:function(e,t,n){"use strict";n(1213)},1245:function(e,t,n){var r=n(35)((function(i){return i[1]}));r.push([e.i,".hero-counter[data-v-093d3de4]{align-items:center;border-bottom-right-radius:1.875rem;border-top-left-radius:.375rem;border-top-right-radius:1.875rem;border-width:1px;display:flex;height:3.125rem;padding-left:.75rem;width:12.5rem;z-index:10}.hero-counter div[data-v-093d3de4]{font-size:1.5rem;font-weight:700;line-height:2rem;margin-right:.3125rem}.hero-counter span[data-v-093d3de4]{font-size:1.125rem;font-weight:300;line-height:1.75rem}",""]),r.locals={},e.exports=r},1258:function(e,t,n){"use strict";n.r(t);n(19),n(21),n(20),n(11),n(25),n(22),n(26);var r=n(0),o=n(13),c=n(1);function l(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable}))),t.push.apply(t,n)}return t}function d(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?l(Object(source),!0).forEach((function(t){Object(r.a)(e,t,source[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):l(Object(source)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))}))}return e}var v={props:{date:{type:String,default:""},bannerId:{type:String,default:""},isCategoryBanner:{type:Boolean,default:!1}},methods:d(d({},Object(o.d)({setHomeFilteredBannerList:Object(c.oe)(c.wd),setHomeCategoryFilteredBannerList:Object(c.oe)(c.vd)})),{},{onFinishHandler:function(){this.isCategoryBanner?this.setHomeCategoryFilteredBannerList(this.bannerId):this.setHomeFilteredBannerList(this.bannerId)}})},f=(n(1244),n(8)),component=Object(f.a)(v,(function(){var e=this,t=e._self._c;return t("BaseCountDownTime",{attrs:{date:e.date,color:"text-gray-600","custom-class":"absolute","is-custom-slot":""},on:{onFinish:e.onFinishHandler},scopedSlots:e._u([{key:"default",fn:function(n){var r=n.days,o=n.hours,c=n.minutes,l=n.seconds,d=n.isLastTenMinutes;return t("div",{staticClass:"hero-counter",class:d?"bg-pink-600 border-pink-600 text-white":"bg-white border-white"},[t("div",{class:{"opacity-50":"00"===r&&("23"!==o||"59"!==c)}},[e._v("\n      "+e._s("59"===c&&"23"===o?parseInt(r)+1:r)),t("span",[e._v("G.")])]),e._v(" "),t("div",{class:{"opacity-50":"00"===r&&"00"===o&&"59"!==c}},[e._v("\n      "+e._s("59"===c?"23"===o?"00":parseInt(o)+1:o)),t("span",[e._v("Sa.")])]),e._v(" "),t("div",{class:{"opacity-50":"00"===r&&"00"===o&&"00"===c&&"00"===l}},[e._v("\n      "+e._s("59"===c?"00":parseInt(c)+1)),t("span",[e._v("Dk.")])])])}}])})}),[],!1,null,"093d3de4",null);t.default=component.exports;installComponents(component,{BaseCountDownTime:n(1227).default})},1319:function(e,t,n){var content=n(1435);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(36).default)("117f06bc",content,!0,{sourceMap:!1})},1434:function(e,t,n){"use strict";n(1319)},1435:function(e,t,n){var r=n(35)((function(i){return i[1]}));r.push([e.i,".hero-side-card[data-v-c65d763e]:not(:last-child){margin-bottom:.9375rem}",""]),r.locals={},e.exports=r},1493:function(e,t,n){var content=n(1603);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(36).default)("7ea54398",content,!0,{sourceMap:!1})},1494:function(e,t,n){var content=n(1605);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(36).default)("0864c66c",content,!0,{sourceMap:!1})},1495:function(e,t,n){var content=n(1607);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(36).default)("2a37d509",content,!0,{sourceMap:!1})},1524:function(e,t,n){"use strict";n.r(t);n(40),n(52);var r={props:{bannerMetaData:{type:Object,default:function(){return{}}},activeBanner:{type:Object,default:function(){return{}}},preventClickTypeList:{type:Array,default:function(){return[]}},externalUrlList:{type:Array,default:function(){return[]}},customClass:{type:[String,Array,Object],default:null}}},o=n(8),component=Object(o.a)(r,(function(){var e=this,t=e._self._c;return e.bannerMetaData.title?t("div",{class:["flex flex-col items-center rounded-md","t1"===e.bannerMetaData.template?"py-2 justify-between":"justify-center",e.customClass]},[t("div",{class:["flex flex-col justify-center items-center max-h-80 overflow-hidden",{"flex-1":"t1"===e.bannerMetaData.template}]},[t("div",{class:["text-center leading-9 font-nexaRegular","t1"===e.bannerMetaData.template?"text-2xl max-w-18":"text-3xl max-w-xs"]},[e._v("\n      "+e._s(e.bannerMetaData.title)+"\n    ")]),e._v(" "),t("div",{class:["text-center leading-normal font-nexaBold","t1"===e.bannerMetaData.template?"text-4xl max-w-18":"text-5xl max-w-xs"]},[e._v("\n      "+e._s(e.bannerMetaData.subTitle)+"\n    ")])]),e._v(" "),t("div",{staticClass:"w-full flex justify-evenly items-center font-nexaBold max-w-xs"},["1"===e.bannerMetaData.counterButton&&e.activeBanner.endDate?t("BaseButton",{attrs:{"custom-class":"!w-30 cursor-default bg-gray-100"}},[t("BaseCountDownTime",{attrs:{"custom-class":"!pr-0",date:e.activeBanner.endDate,"is-custom-slot":!1,"is-timer-button":!0}})],1):e._e(),e._v(" "),e.bannerMetaData.deeplinkButtonTitle?t("BaseLink",{attrs:{color:e.bannerMetaData.buttonColor,tag:e.preventClickTypeList.includes(e.activeBanner.actionType)?"span":e.externalUrlList.includes(e.activeBanner.actionType)?"a":"nuxt-link",to:e.preventClickTypeList.includes(e.activeBanner.actionType)?"":e.activeBanner.seoUrl,"is-external":e.externalUrlList.includes(e.activeBanner.actionType),event:e.preventClickTypeList.includes(e.activeBanner.actionType)?"":"click","custom-class":"btn overflow-hidden w-44 px-1"}},[e._v("\n      "+e._s(e.bannerMetaData.deeplinkButtonTitle)+"\n    ")]):e._e()],1)]):e._e()}),[],!1,null,null,null);t.default=component.exports;installComponents(component,{BaseCountDownTime:n(1227).default,BaseButton:n(55).default,BaseLink:n(63).default})},1525:function(e,t,n){"use strict";n.r(t);n(40),n(52);var r=n(274),o=n.n(r),c=[0,8],l=[7,9],d={name:"HeroSideCard",props:{card:{type:Object,default:function(){return{}}},resize:{type:Object,default:function(){return{}}}},data:function(){return{preventClickTypeList:c,externalUrlList:l}},computed:{placeholderImage:function(){return o.a}}},v=(n(1434),n(8)),component=Object(v.a)(d,(function(){var e=this,t=e._self._c;return t("BaseLink",{attrs:{event:e.preventClickTypeList.includes(e.card.actionType)?"":"click",to:e.preventClickTypeList.includes(e.card.actionType)?"":e.card.seoUrl,tag:e.externalUrlList.includes(e.card.actionType)?"a":"nuxt-link","is-external":e.externalUrlList.includes(e.card.actionType),"custom-class":"relative flex flex-col h-full hero-side-card"}},[t("BaseImg",{attrs:{src:e.card.imageUrl,"placeholder-image":e.placeholderImage,"error-image":e.placeholderImage,"custom-class":"absolute object-contain w-full h-full rounded-md",resize:e.resize,width:"234",height:"92",preload:"",passive:""}})],1)}),[],!1,null,"c65d763e",null);t.default=component.exports;installComponents(component,{BaseImg:n(107).default,BaseLink:n(63).default})},1602:function(e,t,n){"use strict";n(1493)},1603:function(e,t,n){var r=n(35)((function(i){return i[1]}));r.push([e.i,".thumb-swiper{width:95%}.thumb-swiper .swiper-wrapper{margin-left:auto;margin-right:auto;margin-top:1rem;width:-moz-min-content;width:min-content}",""]),r.locals={},e.exports=r},1604:function(e,t,n){"use strict";n(1494)},1605:function(e,t,n){var r=n(35)((function(i){return i[1]}));r.push([e.i,".thumb-swiper-button.swiper-button-prev[data-v-9a1f3e90]{left:-.375rem;top:60%}.thumb-swiper-button.swiper-button-next[data-v-9a1f3e90]{right:-.375rem;top:60%}",""]),r.locals={},e.exports=r},1606:function(e,t,n){"use strict";n(1495)},1607:function(e,t,n){var r=n(35)((function(i){return i[1]}));r.push([e.i,".swiper-overlay-ts-enter-active[data-v-9a1f3e90]{transition:all .2s ease}.swiper-overlay-ts-leave-active[data-v-9a1f3e90]{transition:all .1666666667s ease}.swiper-overlay-ts-enter[data-v-9a1f3e90],.swiper-overlay-ts-leave-to[data-v-9a1f3e90]{opacity:0;transform:translateX(-50px)}.category-title-ts-enter-active[data-v-9a1f3e90]{transition:all .2s ease}.category-title-ts-leave-active[data-v-9a1f3e90]{transition:all .1666666667s ease}.category-title-ts-enter[data-v-9a1f3e90],.category-title-ts-leave-to[data-v-9a1f3e90]{opacity:0;transform:translateY(10px)}",""]),r.locals={},e.exports=r},1698:function(e,t,n){"use strict";n.r(t);n(40),n(52);var r=n(2),o=(n(28),n(75),n(108),n(92),n(44),n(1211)),c=n.n(o),l=[0,8],d=[7,9],v={name:"CategoryBanner",props:{categoryList:{type:Array,default:function(){return[]}},heroSideBannerList:{type:Array,default:function(){return[]}},mainResize:{type:Object,default:function(){return{}}},thumbnailResize:{type:Object,default:function(){return{}}},heroSideCardResize:{type:Object,default:function(){return{}}}},data:function(){return{preventClickTypeList:l,externalUrlList:d,maxHeroSideCard:4,maxHeroBanner:9,isSwiperReady:!1,swiperOptionThumb:{preloadImages:!1,allowTouchMove:!1,slidesPerView:9,spaceBetween:10,lazy:{loadPrevNext:!0,checkInView:!1},showPrev:!1,showNext:!1},activeCategoryIndex:0,activeImageIndex:0,titleHeight:"40px",autoPlayInterval:null,categoryBannerListCount:9}},computed:{thumbSwiper:function(){var e;return null===(e=this.$refs.thumbSwiper)||void 0===e?void 0:e.$swiper},placeholderImage:function(){return c.a},activeBannerList:function(){var e;return null===(e=this.categoryList[this.activeCategoryIndex])||void 0===e?void 0:e.items},activeBannerMetaDataList:function(){return this.activeBannerList.map((function(e){var t,n;return{template:(null==e||null===(t=e.bannerMetaData)||void 0===t?void 0:t.template)||"",backgroundColor:null==e||null===(n=e.bannerMetaData)||void 0===n?void 0:n.backgroundColor}}))},activeBanner:function(){return this.activeBannerList&&this.activeBannerList.length>0?this.activeBannerList[this.activeImageIndex]:{}},sideCardList:function(){return this.heroSideBannerList.slice(0,this.maxHeroSideCard)},bannerMetaData:function(){var e,t,n,r,o,c,l,d,v,f,m,h,w,y,x,_,B,C,I={template:null===(e=this.activeBanner)||void 0===e||null===(t=e.bannerMetaData)||void 0===t?void 0:t.template,title:null===(n=this.activeBanner)||void 0===n||null===(r=n.bannerMetaData)||void 0===r?void 0:r.title,subTitle:null===(o=this.activeBanner)||void 0===o||null===(c=o.bannerMetaData)||void 0===c?void 0:c.subTitle,badgeText:null===(l=this.activeBanner)||void 0===l||null===(d=l.bannerMetaData)||void 0===d?void 0:d.badgeText,deeplinkButtonTitle:null===(v=this.activeBanner)||void 0===v||null===(f=v.bannerMetaData)||void 0===f?void 0:f.deeplinkButtonTitle,badgeBackgroundColor:null===(m=this.activeBanner)||void 0===m||null===(h=m.bannerMetaData)||void 0===h?void 0:h.badgeBackgroundColor,buttonColor:null===(w=this.activeBanner)||void 0===w||null===(y=w.bannerMetaData)||void 0===y?void 0:y.buttonColor,counterButton:null===(x=this.activeBanner)||void 0===x||null===(_=x.bannerMetaData)||void 0===_?void 0:_.counter,backgroundColor:null===(B=this.activeBanner)||void 0===B||null===(C=B.bannerMetaData)||void 0===C?void 0:C.backgroundColor};return I}},watch:{categoryList:{handler:function(){this.activeCategoryIndex=0,this.activeImageIndex=0},deep:!0},activeImageIndex:{handler:function(){this.createGtmViewData()},deep:!0}},mounted:function(){var e=this;return Object(r.a)(regeneratorRuntime.mark((function t(){var n;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,e.$nextTick();case 2:e.titleHeight=(null===(n=e.$refs.bannerWrapper)||void 0===n?void 0:n.scrollHeight)+"px",e.autoPlayHandler(),e.createGtmViewData();case 5:case"end":return t.stop()}}),t)})))()},destroyed:function(){this.changeActiveImage(0)},methods:{changeActiveImage:function(e){clearInterval(this.autoPlayInterval),this.activeImageIndex=e},changeActiveCategoryHandler:function(e){var t=this;return Object(r.a)(regeneratorRuntime.mark((function n(){return regeneratorRuntime.wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return clearInterval(t.autoPlayInterval),t.activeCategoryIndex=e,t.activeImageIndex=0,t.thumbSwiper.slideTo(0),n.next=6,t.$nextTick();case 6:t.thumbSwiper.update(),t.autoPlayHandler();case 8:case"end":return n.stop()}}),n)})))()},nextThumbSwiper:function(e){var t;this.activeImageIndex!==this.activeBannerList.length-1?this.activeImageIndex+=1:clearInterval(this.autoPlayInterval),e&&clearInterval(this.autoPlayInterval),null===(t=this.thumbSwiper)||void 0===t||t.slideNext()},prevThumbSwiper:function(e){var t;0!==this.activeImageIndex&&(this.activeImageIndex-=1),e&&clearInterval(this.autoPlayInterval),null===(t=this.thumbSwiper)||void 0===t||t.slidePrev()},autoPlayHandler:function(){var e=this;this.autoPlayInterval=setInterval((function(){e.nextThumbSwiper()}),5e3)},createGtmClickData:function(){this.$gtmLayer.addLayer("banner","click",{item_id:this.activeBanner.bannerId,item_name:this.activeBanner.name,target_url:this.activeBanner.seoUrl,index:this.activeImageIndex,affiliation:"Pazarama Web",additionalParams:{creative_name:this.activeBanner.seoUrl,creative_slot:this.activeImageIndex,promotion_id:this.activeBanner.bannerId,promotion_name:this.activeBanner.name}},{event:"select_promotion"})},createGtmViewData:function(){this.$gtmLayer.addLayer("banner","view",[{item_id:this.activeBanner.bannerId,item_name:this.activeBanner.name,target_url:this.activeBanner.seoUrl,index:this.activeImageIndex,affiliation:"Pazarama Web",additionalParams:{creative_name:this.activeBanner.seoUrl,creative_slot:this.activeImageIndex,promotion_id:this.activeBanner.bannerId,promotion_name:this.activeBanner.name}}],{event:"view_promotion"})},swiperReady:function(){var e=this;return Object(r.a)(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,e.$nextTick();case 2:e.thumbSwiper.update(),e.isSwiperReady=!0;case 4:case"end":return t.stop()}}),t)})))()}}},f=(n(1602),n(1604),n(1606),n(8)),component=Object(f.a)(v,(function(){var e=this,t=e._self._c;return t("div",{staticClass:"flex flex-col"},[t("div",{ref:"bannerWrapper",staticClass:"flex m-auto mb-5"},e._l(e.categoryList,(function(n,r){return t("div",{key:r,staticClass:"mr-8 text-sm font-medium text-center cursor-pointer",class:{"text-blue-500":r===e.activeCategoryIndex},style:{height:e.titleHeight},on:{click:function(t){return e.changeActiveCategoryHandler(r)}}},[t("div",{staticClass:"px-3 cursor-pointer"},[e._v("\n        "+e._s(n.title)+"\n      ")]),e._v(" "),t("transition",{attrs:{name:"category-title-ts"}},[r===e.activeCategoryIndex?t("div",{staticClass:"bg-blue-500 text-blue-500 h-1 mt-2 rounded-xl"}):e._e()])],1)})),0),e._v(" "),t("div",{staticClass:"flex flex-row"},[t("div",{staticClass:"min-w-984"},["t2"!==e.bannerMetaData.template?t("div",{class:["flex flex-row",{"bg-gray-100 p-2.5 rounded-md":"t1"===e.bannerMetaData.template}]},[t("BaseLink",{attrs:{event:e.preventClickTypeList.includes(e.activeBanner.actionType)?"":"click",to:e.preventClickTypeList.includes(e.activeBanner.actionType)?"":e.activeBanner.seoUrl,"clean-init-class":!0,tag:e.preventClickTypeList.includes(e.activeBanner.actionType)?"span":e.externalUrlList.includes(e.activeBanner.actionType)?"a":"nuxt-link","is-external":e.externalUrlList.includes(e.activeBanner.actionType),"custom-class":["relative",e.preventClickTypeList.includes(e.activeBanner.actionType)?"cursor-default":"cursor-pointer"]},nativeOn:{click:function(t){return e.createGtmClickData()}}},[e.activeBanner.bannerCounter&&e.activeBanner.endDate&&e.isSwiperReady?t("HomeCountDownTime",{attrs:{date:e.activeBanner.endDate,"banner-id":e.activeBanner.bannerId,"is-category-banner":""}}):e._e(),e._v(" "),e.bannerMetaData.badgeText?t("BaseBadge",{attrs:{color:e.bannerMetaData.badgeBackgroundColor,badge:e.bannerMetaData.badgeText,"custom-class":"absolute font-semibold text-sm cursor-default right-0 m-3 py-2 px-3 !pointer-events-none min-w-7"}}):e._e(),e._v(" "),t("BaseImg",{attrs:{src:e.activeBanner.imageUrl,"placeholder-image":e.placeholderImage,"error-image":e.placeholderImage,"custom-class":["rounded-md mx-auto w-1230","t1"===e.bannerMetaData.template?"h-414":"h-415 shadow-lg"],resize:e.mainResize,width:"984",height:"414",preload:"",passive:""}})],1),e._v(" "),"t1"===e.bannerMetaData.template?t("BaseCategoryBannerMetaData",{attrs:{"banner-meta-data":e.bannerMetaData,"active-banner":e.activeBanner,"prevent-click-type-list":e.preventClickTypeList,"external-url-list":e.externalUrlList,"custom-class":"text-black bg-white h-414 w-80 min-w-20 ml-2.5"}}):e._e()],1):t("BaseCategoryBannerMetaData",{style:{"background-color":e.bannerMetaData.backgroundColor},attrs:{"banner-meta-data":e.bannerMetaData,"active-banner":e.activeBanner,"prevent-click-type-list":e.preventClickTypeList,"external-url-list":e.externalUrlList,"custom-class":"text-white h-415 pt-3"}}),e._v(" "),t("keep-alive",[t("div",{staticClass:"relative"},[t("Swiper",{ref:"thumbSwiper",staticClass:"thumb-swiper",attrs:{options:e.swiperOptionThumb,"auto-update":!1,"auto-destroy":!1},on:{ready:e.swiperReady}},e._l(e.activeBannerList,(function(n,r){return t("SwiperSlide",{key:r},["t2"===e.activeBannerMetaDataList[r].template?t("div",{staticClass:"mx-auto w-24 h-12.5 cursor-pointer rounded",style:{"background-color":e.activeBannerMetaDataList[r].backgroundColor},on:{click:function(t){return e.changeActiveImage(r)}}}):t("BaseImg",{attrs:{src:n.imageUrl_TH,"placeholder-image":e.placeholderImage,"error-image":e.placeholderImage,"custom-class":"mx-auto w-25 h-12.5 cursor-pointer rounded",resize:e.thumbnailResize},nativeOn:{click:function(t){return e.changeActiveImage(r)}}}),e._v(" "),t("transition",{attrs:{name:"swiper-overlay-ts"}},[e.activeImageIndex===r?t("div",{staticClass:"absolute rounded bg-blue-500/50 w-full h-full top-0"}):e._e()])],1)})),1),e._v(" "),t("div",{directives:[{name:"show",rawName:"v-show",value:e.isSwiperReady&&e.activeBannerList.length>e.maxHeroBanner,expression:"isSwiperReady && activeBannerList.length > maxHeroBanner"}],staticClass:"thumb-swiper-button swiper-button-prev",on:{click:function(t){return e.prevThumbSwiper(!0)}}},[t("BaseSvg",{attrs:{file:"arrow-angle-left",color:e.activeImageIndex>0?"text-blue-500":"text-gray-400","custom-class":"shadow",size:8}})],1),e._v(" "),t("div",{directives:[{name:"show",rawName:"v-show",value:e.isSwiperReady&&e.activeBannerList.length>e.maxHeroBanner,expression:"isSwiperReady && activeBannerList.length > maxHeroBanner"}],staticClass:"thumb-swiper-button swiper-button-next",on:{click:function(t){return e.nextThumbSwiper(!0)}}},[t("BaseSvg",{attrs:{file:"arrow-angle-right",color:e.activeImageIndex<e.activeBannerList.length-1?"text-blue-500":"text-gray-400","custom-class":"shadow",size:8}})],1)],1)])],1),e._v(" "),t("div",{staticClass:"w-full ml-3 h-415 flex flex-col justify-between"},e._l(e.sideCardList,(function(n,r){return t("BaseHeroSideCard",{key:r,attrs:{card:n,resize:e.heroSideCardResize}})})),1)])])}),[],!1,null,"9a1f3e90",null);t.default=component.exports;installComponents(component,{HomeCountDownTime:n(1258).default,BaseBadge:n(271).default,BaseImg:n(107).default,BaseLink:n(63).default,BaseCategoryBannerMetaData:n(1524).default,BaseSvg:n(74).default,BaseHeroSideCard:n(1525).default})}}]);