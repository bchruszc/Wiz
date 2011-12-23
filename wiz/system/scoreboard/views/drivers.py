#from django.shortcuts import render_to_response
#from django.template import RequestContext
#
#from system.pool.models import Driver
#from system.pool.models import Finish
#from system.pool.models import DrivesForTeam
#from system.pool.models import Race
#
#def drivers(request, driver_id=-1): 
#    driver_list = Driver.objects.with_points()
#    driver_list_alpha = Driver.objects.all().order_by('first_name')
#
#    if driver_id == -1:
#        
#        driver = None
#        finishes = None
#        owners = None
#        
#        last_pts = 0
#        last_rank = 0
#        x = 0
#        for d in driver_list:
#          x = x + 1
#          d.rank = x
#          if d.total_points == 0:
#            d.dollars_per_point = 0
#          else:
#            d.dollars_per_point = d.value / d.total_points
#            
#          if d.total_points == last_pts:
#            d.rank = last_rank
#          else:
#            last_rank = x
#            last_pts = d.total_points
#    else:
#        driver = Driver.objects.get(id=driver_id)
#        finishes = Finish.objects.filter(driver=driver_id).order_by('race') #@UndefinedVariable
#        allDFT = DrivesForTeam.objects.all() #@UndefinedVariable
#        owners = allDFT.filter(driver=driver_id) & allDFT.filter(race=Race.objects.get(week=36).id) #@UndefinedVariable
#        
#    return render_to_response('pool/drivers.html', RequestContext(request, {
#            'menu_group':"drivers",
#            'drivers':driver_list,
#            'drivers_alpha':driver_list_alpha,
#            'driver':driver,
#            'finishes':finishes,
#            'owners':owners,
#        }))
