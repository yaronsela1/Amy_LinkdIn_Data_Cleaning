PATH = 'C:\\Users\\yaron\\Desktop\\Amy\\dan_pastor_bug.txt'
PATH2 = 'C:\\Users\\yaron\\Desktop\\Amy\\nimrod_education.txt'
CREATE_PATH = 'C:\\Users\\yaron\\Desktop\\Amy\\nimrod_new.txt'
CREATE_PATH2 = 'C:\\Users\\yaron\\Desktop\\Amy\\dan_new.txt'
# TODO: Create config file with all the const values


def multiple_jobs_same_company(i, company, lines, company_lst, position_lst, dates_employed_lst):
    company_checker = "Company Name"
    date_checker = "Dates Employed"
    while lines[i + 1].startswith(company_checker) == False:
        if lines[i].startswith(date_checker):
            company_lst.append(company)

            position = lines[i-1].lstrip('Title').rstrip('\n')
            position_lst.append(position)

            date = lines[i].replace(date_checker, '').replace('â€“',
                                                                  '-')  # TODO: check if there is a cleaner way to do this
            dates_employed_lst.append(date)
        i += 1
    return company_lst, position_lst, dates_employed_lst, i


def clean_linkedin_copied_work_experience(file_path):
    company_lst = []
    position_lst = []
    dates_employed_lst = []
    company_checker = "Company Name"
    date_checker = "Dates Employed"
    with open(file_path, 'r', encoding="utf8") as f:  # TODO: Split into companies first then process the output
        lines = f.readlines()
        i = 0
        while i < len(lines)-2:

            if lines[i + 2].startswith("Total Duration"):
                company = lines[i].rstrip('\n')
                i += 2
                company_lst, position_lst, dates_employed_lst, i = \
                    multiple_jobs_same_company(i, company, lines, company_lst, position_lst, dates_employed_lst)


            if lines[i + 1].startswith(company_checker):
                company = lines[i - 1].rstrip('\n')
                company_lst.append(company)


                position = lines[i].rstrip('\n')
                position_lst.append(position)

                date = lines[i+2].replace(date_checker, '').replace('â€“', '-') # TODO: check if there is a cleaner way to do this
                dates_employed_lst.append(date)
            i += 1
    return company_lst, position_lst, dates_employed_lst


def clean_linkedin_copied_education(file_path):
    degree_checker = 'Degree Name'
    date_checker = 'Dates attended or expected graduation'
    degree_lst = []
    uni_lst = []
    date_lst = []
    with open(file_path, 'r', encoding="utf8") as f:
        lines = f.readlines()
        for i in range(len(lines)-1):
            if lines[i].startswith(degree_checker):
                degree = lines[i].replace(degree_checker, '').replace('Field Of Study', ', ').rstrip('\n')
                degree_lst.append(degree)

                university = lines[i - 1].rstrip('\n')
                uni_lst.append(university)

                date = lines[i+1].replace(date_checker, '').replace('â€“', '-')
                date_lst.append(date)
    return degree_lst, uni_lst, date_lst


def finalize_linkedin_copied_work_experience(company_lst, position_lst, dates_employed_lst):
    experience_lst = []
    for i in range(len(company_lst)):
        if dates_employed_lst[i].endswith(' - Present'):
            dates_employed_lst[i] = dates_employed_lst[i].rstrip(' - Present')
            dates_employed_lst[i] = 'Since ' + dates_employed_lst[i]
        experience = company_lst[i] + ' (' + position_lst[i] + ') ' + dates_employed_lst[i]
        experience_lst.append(experience)
    return experience_lst


def finalize_linkedin_copied_education(degree_lst, uni_lst, date_lst):
    education_lst = []
    for i in range(len(degree_lst)):
        education = degree_lst[i] + ' (' + uni_lst[i] + ') ' + date_lst[i]
        education_lst.append(education)
    return education_lst


def brief(path, create_path):
    company_lst, position_lst, dates_employed_lst = clean_linkedin_copied_work_experience(path)
    degree_lst, uni_lst, date_lst = clean_linkedin_copied_education(path)
    with open(create_path, 'w+') as f:
        f.write('Experience\n\n')

        experience_lst = finalize_linkedin_copied_work_experience(company_lst, position_lst, dates_employed_lst)
        education_lst = finalize_linkedin_copied_education(degree_lst, uni_lst, date_lst)

        for line in experience_lst:
            f.write(line)

        f.write('\nEducation\n\n')
        for line in education_lst:
            f.write(line)

if __name__ == '__main__':
    brief(PATH, CREATE_PATH2)  # TODO: Use arguments and not a const path




