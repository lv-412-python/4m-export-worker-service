"""Set permission to user."""
from apiclient import errors


def insert_permission(service, file_id, value, perm_type, role):
    """Insert a new permission.
    Args:
      service: Drive API service instance.
      file_id: ID of the file to insert permission for.
      value: User or group e-mail address, domain name or None for 'default'
             type.
      perm_type: The value 'user', 'group', 'domain' or 'default'.
      role: The value 'owner', 'writer' or 'reader'.
    Returns:
      The inserted permission if successful, None otherwise.
    """
    new_permission = {
        'emailAddress': value,
        'type': perm_type,
        'role': role,
        'transferOwnership': True
    }
    response = None
    try:
        response = service.permissions().create(
            fileId=file_id, body=new_permission).execute()
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
    return response
