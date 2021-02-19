import os
from jinja2 import Template
from yaasr import get_all_streams


def setup_supervisor(stream_name,
                     system_user_name,
                     google_credentials_path,
                     total_seconds=0,
                     chunk_bytes_size=256,
                     chunk_time_size=30 * 60):

    """ setup supervisor to save a radio station. """
    streams = get_all_streams() if stream_name.lower() == 'all' else [stream_name]
    template_file = os.path.join(os.path.dirname(__file__), 'tpl', 'supervisor.ini')
    context = {
        'user_name': system_user_name,
        'google_credentials_path': google_credentials_path,
        'total_seconds': total_seconds,
        'chunk_bytes_size': chunk_bytes_size,
        'chunk_time_size': chunk_time_size
    }
    template = Template(open(template_file).read())
    for stream in streams:
        context['stream_name'] = stream
        result = template.render(**context)
        path = f'/etc/supervisor/conf.d/{stream}.conf'
        f = open(path, 'w')
        f.write(result)
        f.close()

        print(f'{path} was created. Run "sudo supervisorctl start yaasr-{stream}" to start recording audios')
