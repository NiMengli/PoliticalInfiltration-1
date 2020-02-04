# -*- coding: utf-8 -*-

from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
import time
import datetime
from collections import defaultdict

from Userprofile.models import *
from Mainevent.models import *
from Config.base import *

from rest_framework.views import APIView
from rest_framework.schemas import ManualSchema


class Test(APIView):
    """测试页面"""

    def get(self, request):
        """GET方法的功能说明写在这里"""
        return HttpResponse('这是测试的GET方法')

    def post(self, request):
        """POST方法的功能说明写在这里"""
        return HttpResponse('这是测试的POST方法')

    def put(self, request):
        """PUT方法的功能说明写在这里"""
        return HttpResponse('这是测试的PUT方法')

    def delete(self, request):
        """DELETE方法的功能说明写在这里"""
        return HttpResponse('这是测试的DELETE方法')


class BasicInfo(APIView):
    """用户基本信息接口"""

    def get(self, request):
        """
        获取uid，返回用户详情;
        格式: {"uid": uid, "nick_name": nick_name,...}
        """
        res_dict = {}
        uid = request.GET.get('uid')
        result = Figure.objects.filter(f_id=uid).first()
        res_dict["uid"] = result.uid if result.uid else "无"
        res_dict["nick_name"] = result.nick_name if result.nick_name else "无"
        res_dict["age"] = datetime.date.today().year - result.user_birth.year if result.user_birth else "无"
        # now = datetime.date.today()
        # birth = result.user_birth
        # if now.month < birth.month:  # 如果月份比今天大，没过生日，则年份相减再减一
        #     res_dict["age"] = now.year - birth.year - 1
        # if now.month > birth.month:  # 如果月份比今天小，过生日了，则年份相减
        #     res_dict["age"] = now.year - birth.year
        # if now.month == birth.month and now.day < birth.day:  # 如果月份相等，生日比今天大，没过生日
        #     res_dict["age"] = now.year - birth.year - 1
        # if now.month == birth.month and now.day > birth.day:  # 如果月份相等，生日比今天小，过生日了
        #     res_dict["age"] = now.year - birth.year
        res_dict["statusnum"] = result.statusnum if result.statusnum else "无"
        res_dict["political"] = political_dict[result.political] if result.political else "无"
        # res_dict["domain"] = result.domain if result.domain else "无"
        domain = list(UserDomain.objects.filter(uid=uid).values("main_domain").order_by("-timestamp"))[0]["main_domain"]
        res_dict["domain"] = domain_dict[domain] if domain else "无"
        res_dict["create_at"] = time.strftime("%Y-%m-%d", time.localtime(result.create_at)) if result.create_at else "无"
        res_dict["sex"] = ("男" if result.sex == 1 else "女") if result.sex else "无"
        res_dict["friendsnum"] = result.friendsnum if result.friendsnum else "无"
        res_dict["fansnum"] = result.fansnum if result.fansnum else "无"
        res_dict["user_location"] = result.user_location if result.user_location else "无"
        res_dict["description"] = result.description if len(result.description) != 0 else "无"
        return JsonResponse(res_dict)

    def post(self, request):
        """"""
        return HttpResponse('这是POST方法')


class User_Behavior(APIView):
    """用户活动特征接口"""

    def get(self, request):
        """
        获取uid，返回用户活动特征详情，根据传入参数n_type 日 周 月 返回相应数据结果，
        返回数据格式{date1:{originalnum_s:10,commentnum_s:20,retweetnum_s:30,sensitivenum_s:10},
                    date2:{originalnum_s: 10,commentnum_s:20,retweetnum_s:30,sensitivenum_s:10},
                    ...}
        """
        uid = request.GET.get('uid')
        n_type = request.GET.get('n_type')
        res_dict = {}
        # 每日活动特征，从当前日期往前推7天展示 原创微博数、评论数、转发数、敏感微博数
        if n_type == "日":
            new_date = (datetime.datetime.now() + datetime.timedelta(days=-7)).timestamp()
            result = UserBehavior.objects.filter(uid=uid, timestamp__gte=new_date).values(
                "timestamp").annotate(originalnum_s=Sum("originalnum"), commentnum_s=Sum("commentnum"),
                                      retweetnum_s=Sum("retweetnum"), sensitivenum_s=Sum("sensitivenum"))
            for item in result:
                t = item.pop("timestamp") - 24 * 60 * 60
                res_dict[time.strftime("%Y-%m-%d", time.localtime(t))] = item
        # 每周活动特征，从当前日期往前推5周展示 原创微博数、评论数、转发数、敏感微博数
        if n_type == "周":
            date_dict = {}
            for i in range(5):
                date_dict[i + 1] = (datetime.datetime.now() + datetime.timedelta(weeks=(-1 * (i + 1)))).timestamp()
            date_dict[0] = time.time()
            for i in range(5):
                result = UserBehavior.objects.filter(uid=uid, timestamp__gte=date_dict[i + 1],
                                                     timestamp__lt=date_dict[i]).aggregate(
                    originalnum_s=Sum("originalnum"), commentnum_s=Sum("commentnum"), retweetnum_s=Sum("retweetnum"),
                    sensitivenum_s=Sum("sensitivenum"))
                if list(result.values())[0]:
                    res_dict[time.strftime("%Y-%m-%d", time.localtime((date_dict[i]) - 24 * 60 * 60))] = result
        # 每月活动特征，从当前日期往前推5月展示 原创微博数、评论数、转发数、敏感微博数
        if n_type == "月":
            date_dict = {}
            for i in range(5):
                date_dict[i + 1] = (datetime.datetime.now() + datetime.timedelta(days=(-30 * (i + 1)))).timestamp()
            date_dict[0] = time.time()
            for i in range(5):
                result = UserBehavior.objects.filter(uid=uid, timestamp__gte=date_dict[i + 1],
                                                     timestamp__lt=date_dict[i]).aggregate(
                    originalnum_s=Sum("originalnum"), commentnum_s=Sum("commentnum"), retweetnum_s=Sum("retweetnum"),
                    sensitivenum_s=Sum("sensitivenum"))
                if list(result.values())[0]:
                    res_dict[time.strftime("%Y-%m-%d", time.localtime((date_dict[i]) - 24 * 60 * 60))] = result
        return JsonResponse(res_dict)


class User_Activity(APIView):
    """用户地域特征接口"""

    def get(self, request):
        """
        获取uid，返回用户地域特征详情，根据地理位置、IP段，展示当日、前7天、前30天、前90天敏感微博数降序排序;
        n_type对应关系,默认n_type=3:
                        {"1":day_date,"2":week_date,"3":month_date,"4":threemonth_date}
        返回数据格式{
                    "day_result":[{"geo1":geo_name,"send_ip":ips,"statusnum_s":30,"sensitivenum_s":10},{},...],
                    "geo_map_result":[{"geo1":geo_name,"statusnum_s":30},{},..],
                    "route_list":[{"s":geo,"e":geo},{s":geo,"e":geo},...]
                }
        """
        uid = request.GET.get('uid')
        n_type = request.GET.get('n_type') if request.GET.get('n_type') else 3
        res_dict = {}
        cal_date = (datetime.datetime.now() + datetime.timedelta(days=-30)).timestamp()
        if n_type == 1:
            cal_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).timestamp()
        elif n_type == 2:
            cal_date = (datetime.datetime.now() + datetime.timedelta(days=-7)).timestamp()
        elif n_type == 3:
            cal_date = (datetime.datetime.now() + datetime.timedelta(days=-30)).timestamp()
        elif n_type == 4:
            cal_date = (datetime.datetime.now() + datetime.timedelta(days=-90)).timestamp()

        day_result = UserActivity.objects.filter(uid=uid, timestamp__gte=cal_date).values("geo", "send_ip").annotate(
            statusnum_s=Sum("statusnum"), sensitivenum_s=Sum("sensitivenum")).order_by("-sensitivenum_s")
        res_dict["day_result"] = list(day_result)
        # 活动轨迹部分，如展示有问题可去掉
        geo_dict = UserActivity.objects.filter(uid=uid, timestamp__gte=cal_date).values("timestamp", "geo").annotate(
            statusnum_s=Sum("statusnum"))
        route_dict = defaultdict(dict)
        for item in geo_dict:
            t = item.pop("timestamp")
            route_dict[t][item["geo"]] = item["statusnum_s"]
        geo_dict_item = list(route_dict.items())
        route_list = []
        geo_dict_item = sorted(geo_dict_item, key=lambda x: x[0])
        geo_index = 0
        for i in range(len(geo_dict_item)):
            if not geo_dict_item[i][1]:
                continue
            item = {'s': max(geo_dict_item[i][1], key=geo_dict_item[i][1].get).split('&')[1], 'e': ''}
            route_list.append(item)
            if geo_index > 0:
                route_list[geo_index - 1]['e'] = max(geo_dict_item[i][1], key=geo_dict_item[i][1].get).split('&')[1]
            geo_index += 1
        if len(route_list) > 1:
            del (route_list[-1])
        elif len(route_list) == 1:
            route_list[0]['e'] = route_list[0]['s']
        for item in route_list:
            if not (item['s'] and item['e']):
                route_list.remove(item)
        res_dict["route_list"] = route_list

        # 热度展示
        geo_map_result = UserActivity.objects.filter(uid=uid, timestamp__gte=cal_date).values("geo").annotate(
            statusnum_s=Sum("statusnum")).order_by("-statusnum_s")
        res_dict["geo_map_result"] = list(geo_map_result)

        return JsonResponse(res_dict)


class Association(APIView):
    """用户关联分析接口"""

    def get(self, request):
        """
        获取uid，返回用户关联分析详情，包括用户参与的相关事件、相关信息详情,
        数据格式{
                    "event":[{"event_name": event_name1, "keywords": keywords_dict1},{}],
                    "information":[{"text": text1, "hazard_index": hazard_index1, "mid": i.mid},{}]
                }
        """
        res_dict = defaultdict(list)
        uid = request.GET.get('uid')
        res_event = Figure.objects.filter(f_id=uid).first().event_set.all()
        for e in res_event:
            res_dict["event"].append({"event_name": e.event_name, "keywords": e.keywords_dict})
        res_information = Information.objects.filter(uid=uid)
        for i in res_information:
            res_dict["information"].append({"text": i.text, "hazard_index": i.hazard_index, "mid": i.mid})
        return JsonResponse(res_dict)




def insertData(e_name, *figure_names):
    cour_name = []

    for f in figure_names:
        try:
            figure = Figure.objects.get(uid=f)
        except Figure.DoesNotExist:
            figure = Figure.objects.create(uid=f)
        cour_name.append(figure)
    e = Event(e_id=str(int(time.time())), event_name=e_name, begin_timestamp=10110000, begin_date=datetime.date.today())
    e.save()
    e.figure.add(*cour_name)


class Show_prefer(APIView):
    def get(self,request):
        re = defaultdict(list)
        re2 = defaultdict(list)
        prefer = defaultdict(dict)
        uid = request.GET.get("uid")
        #start_time = request.GET.get("time1")
        #end_time = request.GET.get("time2")
        result1 = UserTopic.objects.filter(uid = uid)  #, store_date__range=(start_time,end_time)
        result2 = UserDomain.objects.filter(uid = uid)  #, store_date__range=(start_time,end_time)
        #return HttpResponse(typeof(result))
        if result1.exists():
            json_data = serializers.serialize("json",result1)
            results = json.loads(json_data)
            #return JsonResponse(results,safe=False)
            '''
            count = np.zeros(19)
            for i in results:
                #return JsonResponse(i,safe=False)
                i["fields"]["topics"]["art"] += count[0]
                count[0] = i["fields"]["topics"]["art"]
                i["fields"]["topics"]["computer"]+= count[1]
                count[1] = i["fields"]["topics"]["computer"]
                i["fields"]["topics"]["economic"] += count[2]
                count[2] = i["fields"]["topics"]["economic"]
                i["fields"]["topics"]["education"] += count[3]
                count[3] = i["fields"]["topics"]["education"]
                i["fields"]["topics"]["environment"] += count[4]
                count[4] = i["fields"]["topics"]["environment"]
                i["fields"]["topics"]["medicine"] += count[5]
                count[5] = i["fields"]["topics"]["medicine"]
                i["fields"]["topics"]["military"] += count[6]
                count[6] = i["fields"]["topics"]["military"]
                i["fields"]["topics"]["politics"] += count[7]
                count[7] = i["fields"]["topics"]["politics"]
                i["fields"]["topics"]["sports"] += count[8]
                count[8] = i["fields"]["topics"]["sports"]
                i["fields"]["topics"]["traffic"] += count[9]
                count[9] = i["fields"]["topics"]["traffic"]
                i["fields"]["topics"]["life"] += count[10]
                count[10] = i["fields"]["topics"]["life"]
                i["fields"]["topics"]["anti-corruption"] += count[11]
                count[11] = i["fields"]["topics"]["anti-corruption"]
                i["fields"]["topics"]["employment"] += count[12]
                count[12] = i["fields"]["topics"]["employment"]
                i["fields"]["topics"]["fear-of-violence"] += count[13]
                count[13] = i["fields"]["topics"]["fear-of-violence"]
                i["fields"]["topics"]["house"] += count[14]
                count[14] = i["fields"]["topics"]["house"]
                i["fields"]["topics"]["law"] += count[15]
                count[15] = i["fields"]["topics"]["law"]
                i["fields"]["topics"]["peace"] += count[16]
                count[16] = i["fields"]["topics"]["peace"]
                i["fields"]["topics"]["religion"] += count[17]
                count[17] = i["fields"]["topics"]["religion"]
                i["fields"]["topics"]["social-security"] += count[18]
                count[18] = i["fields"]["topics"]["social-security"]
                re.append(i["fields"]["topics"])
            '''
            for i in results:
                uid = i["fields"]["uid"]
                re[uid].append(i["fields"]["topics"])
            #re = sorted(re.values()[0],key=lambda x:x[1],reverse=True)[:5]
            prefer['topic'] = re
            #result = sorted(result[0], reverse = True)
            #return HttpResponse(re)
        #if result2.exists():
            json_data2 = serializers.serialize("json",result2)
            results2 = json.loads(json_data2)
            for i in results2:
                #re2[i['fields']['uid']].append(i["fields"]["domains"])  #,{"main_domain":i["fields"]["main_domain"]}
                re2[i['fields']['uid']].append({"main_domain":i["fields"]["main_domain"]})
            #re2 = sorted(re2.items(),key=lambda x:x[1],reverse=True)[:5]
            prefer['domain'] = re2
            return JsonResponse(prefer,safe=False)
        else:
            return JsonResponse({"status":400, "error": "未找到该用户信息"},safe=False,json_dumps_params={'ensure_ascii':False}) 


class Show_keyword(APIView):
    def get(self,request):
        re1 = defaultdict(list)
        uid = request.GET.get("uid")
        #start_time = request.GET.get("time1")
        #end_time = request.GET.get("time2")
        result = UserKeyWord.objects.filter(uid = uid)  #, store_date__range=(start_time,end_time)
        #return HttpResponse(typeof(result))
        if result.exists():
            json_data = serializers.serialize("json",result)
            results = json.loads(json_data)
            #return JsonResponse(results,safe=False)
            for i in results:
                uid = i["fields"]["uid"]
                #re1[uid].append({"keywords":i["fields"]["keywords"],"sensitive_words":i["fields"]["sensitive_words"],"hastags":i["fields"]["hastags"]})
                re1[uid] = {"keywords":i["fields"]["keywords"],"sensitive_words":i["fields"]["sensitive_words"],"hastags":i["fields"]["hastags"]}
            return JsonResponse(re1,safe=False,json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse({"status":400, "error": "未找到该用户信息"},safe=False,json_dumps_params={'ensure_ascii':False})

class Show_contact(APIView):
    def get(self,request):
        user_source=defaultdict(list)
        user_target=defaultdict(list)
        insource = []
        outsource = []
        intarget = []
        outtarget = []
        uid = request.GET.get("uid")
        start_time = request.GET.get("time1")
        #end_time = request.GET.get("time2")
        days = request.GET.get("days")
        result1 = UserSocialContact.objects.filter(target = uid, store_date__range=(start_time,start_time-days))\
                   .values('source').annotate(c=Count('uid')).filter(c__gte=1)
        result2 = UserSocialContact.objects.filter(source = uid, store_date__range=(start_time,start_time-days))\
                   .values('target').annotate(c=Count('uid')).filter(c__gte=1)
        if result1.exists():
            for re in result1:
                test = Figure.objects.filter(uid=re['source'])
                if test.exists():
                    insource.append(re['source'])
                    #user_source["in"].append({'uid':re['uid'],'insource':re['source']})
                else:
                    outsource.append(re['source'])
                    #user_source["out"].append('outsource':re['source'])
            #json_source = serializers.serialize("json",in_)
            #results1 = json.loads(json_source)
        if result2.exists():
            for re in result2:
                test = Figure.objects.filter(uid=re['target'])
                if test.exists():
                    intarget.append(re['target'])
                    #user_source["in"].append({"uid":re["uid"],'intarget':re['target']})
                else:
                    outtarget.append(re['target'])
                    #user_source["out"].append({'uid':re['uid'],'outtarget':re['target']})
        user_source["in"].append("uid":uid,'intarget':outtarget,'insource':outsource)
        user_source["out"].append("uid":uid,'outtarget':outtarget,'outsource':outsource)
        return JsonResponse(user_source,safe=False)
        '''else:
            return JsonResponse({"status":400, "error": "未找到符合条件的用户"},safe=False,json_dumps_params={'ensure_ascii':False})
<<<<<<< Updated upstream

=======
        '''

class Figure_create(APIView):
    """添加人物入库和删除人物"""
# status 0->未计算 1->已计算 2->计算中 3->计算失败
    def get(self,request):
        """添加人物：获取添加信息，输入uid,nick,location,fans,friends,political,domain
           调取人物id、昵称、注册地、粉丝数、关注数、政治倾向和领域，若没有填写微博ID则wb_id="";输出状态及提示：400 状态错误，201写入成功"""
        times = int(time.time())
        dates = datetime.datetime.now().strftime('%Y-%m-%d')  # 获取当前时间戳和日期
        f_id = request.GET.get("uid") #f_id与uid均为输入的用户id
        uid = request.GET.get("uid")  
        nick = request.GET.get("nick")
        location = request.GET.get("location")
        fans = request.GET.get("fans")
        friends = request.GET.get("friends")
        political = request.GET.get("political")
        domain = request.GET.get("domain")
        #h_id = request.GET.get("wb_id")  # 若该条人工输入事件从微博而来 则需输入来源微博的id
        #result = Task.objects.filter(~Q(mid=''), mid=h_id) #判断从微博得来的事件是否已存在，若微博ID未给出返回一个空值
        if f_id and nick :
            Figure.objects.create(f_id=f_id, uid=uid, nick_name=nick,user_location=location,fansnum=fans,
                                friendsnum=friends,political = political,domain=domain)
            return JsonResponse({"status":201, "msg": "人物添加成功"},safe=False,json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse({"status":400, "error": "请输入人物的相关信息"},safe=False,json_dumps_params={'ensure_ascii':False})


class Figure_delete(APIView):
# 选中要删除的人物 选中时传入uid 
    def get(self,request):
        uid = request.GET.get("uid")
        result = Figure.objects.filter(f_id=uid)
        if result.exists():
            try:
                Figure.objects.filter(f_id=uid).delete() 
                return JsonResponse({"status":201, "msg": "人物已删除"},safe=False,json_dumps_params={'ensure_ascii':False})
            except:
                return JsonResponse({"status":400, "error": "删除失败"},safe=False,json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse({"status":400, "error": "人物不存在"},safe=False,json_dumps_params={'ensure_ascii':False})



class Show_figure(APIView):
    """展示人物列表"""
    def get(self, request):
        """展示人物,该文档返回Figure表中存在的需要展示的数据，返回字段f_id为用户账号，nick_name为昵称
          fansnum粉丝数,friendsnum关注数,political政治倾向,domain领域,user_location地点"""
        result = Figure.objects.values("f_id","nick_name","fansnum",'friendsnum','political','domain','user_location')
        return HttpResponse(result)



class search_figure(APIView):
    """展示所搜寻人物信息"""
    def get(self, request):
        """展示人物,该文档返回Figure表中存在的需要展示的数据，返回字段f_id为用户账号，nick_name为昵称
          fansnum粉丝数,friendsnum关注数,political政治倾向,domain领域,user_location地点"""
        name = request.GET.get("nick")
        result = Figure.objects.filter(nick_name__contains = name).values("f_id","nick_name","fansnum",'friendsnum','political','domain','user_location')
        return HttpResponse(result)

