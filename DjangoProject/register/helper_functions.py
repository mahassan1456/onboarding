
def user_directory_path_hospital(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'register/{0}/{1}'.format(instance.name,filename)