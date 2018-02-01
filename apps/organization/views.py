from django.shortcuts import render
from django.views.generic.base import View
from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


# 处理课程机构列表的view
class OrgView(View):
    def get(self, request):
        # 取出所有的城市
        all_citys = CityDict.objects.all()
        # 共计多少家机构
        all_num = CourseOrg.objects.count()
        # 查找到所有的课程机构
        all_orgs = CourseOrg.objects.all()
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_orgs中取五个出来，每页显示5个
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        city_id = request.GET.get('city', '')
        if city_id:
            # 外键city在数据中叫city_id，我们就进一步筛选
            all_org = all_orgs.filter(city_id=int(city_id))
        category = request.GET.get('ct', "")
        if category:
            # 我们就在机构中作进一步筛选类别
            all_orgs = all_orgs.filter(category=category)
        # 总共有多少家机构使用count进行统计
        org_nums = all_orgs.count()

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        return render(request, "org_list.html", {
            'all_citys': all_citys,

            'all_orgs': all_orgs,
            'city_id': city_id,
            "category": category,
            'org_nums': org_nums,
            "sort": sort,



        })

