

def getBreakdownByUserType(self_,response, choice):
    displayStartDate = self_.end_date
    all_total = 0
    #if self_.breakdown_item in [choice.PARTNER.capitalize(), choice.MONTH, choice.WEEK]:
    if self_.partners.count() > 1 and self_.locations.count() > 1 and len(self_.user_type) > 1:
        # curr_total = self_.queryset.filter(
        #     created__date__gte=start_date_,
        #     created__date__lte=week_end_date
        # ).count()
        # all_total += curr_total
        print("self_.partners1={}".format(self_.partners))
        # for partner in self_.partners:
        #     curr_total = self_.queryset.filter(
        #         partner=partner
        #     ).count()
        #     all_total += curr_total
        #     response.append(
        #         {
        #             'partner': partner.name,
        #             'total': curr_total,
        #         }
        #     )

        individuals_count = self_.queryset.filter(
            account_type=choice.INDIVIDUAL
        ).count()
        group_count = self_.queryset.filter(
            account_type=choice.GROUP
        ).count()
        all_total = all_total + individuals_count + group_count
        response.append(
            {
                'individuals_count': individuals_count,
                'group_count': group_count,
                'total': all_total,
            }
        )
    elif self_.partners.count() == 1 and self_.locations.count() > 1 and len(self_.user_type) > 1:
        individuals_count = self_.queryset.filter(
            account_type=choice.INDIVIDUAL,
            partner__in=self_.partners
        ).count()
        group_count = self_.queryset.filter(
            account_type=choice.GROUP,
            partner__in=self_.partners
        ).count()
        all_total = all_total + individuals_count + group_count
        response.append(
            {
                'individuals_count': individuals_count,
                'group_count': group_count,
                'total': all_total,
            }
        )

    elif self_.partners.count() == 1 and self_.locations.count() == 1 and len(self_.user_type) > 1:
        data = self_.queryset.filter(
            partner__in=self_.partners,
            location__in=self_.locations,
            account_type__in=self_.user_type
        )
        individuals_count = data.filter(
            account_type=choice.INDIVIDUAL
        ).count()
        group_count = data.filter(
            account_type=choice.GROUP
        ).count()
        all_total = all_total + individuals_count + group_count
        response.append(
            {
                'individuals_count': individuals_count,
                'group_count': group_count,
                'total': all_total,
            }
        )
    elif self_.partners.count() == 1 and self_.locations.count() == 1 and len(self_.user_type) == 1:
        data = self_.queryset.filter(
            partner__in=self_.partners,
            location__in=self_.locations,
            account_type__in=self_.user_type
        )
        individuals_count = data.filter(
            account_type=choice.INDIVIDUAL
        ).count()
        group_count = data.filter(
            account_type=choice.GROUP
        ).count()
        all_total = all_total + individuals_count + group_count
        response.append(
            {
                'individuals_count': individuals_count,
                'group_count': group_count,
                'total': all_total,
            }
        )
    # response[0]['all_total'] = all_total
    try:
        response[0]['all_total'] = all_total
    except Exception as e:
        response.append({
            'start_date': displayStartDate,
            'total': 0,
            'all_total': 0
        })

    return response