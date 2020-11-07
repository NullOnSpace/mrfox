# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import json
import logging
import subprocess

from urllib.parse import parse_qs

import requests
from OpenSSL.crypto import verify, load_publickey, FILETYPE_PEM, X509
from OpenSSL.crypto import Error as SignatureError

from django.shortcuts import render
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponseBadRequest, JsonResponse

logger = logging.getLogger(__name__)

class Travis(View):

    # Make sure you use the correct config URL, the .org and .com
    # have different keys!
    # https://api.travis-ci.org/config
    # https://api.travis-ci.com/config
    TRAVIS_CONFIG_URL = settings.TRAVIS_CONFIG_URL

    def post(self, request, *args, **kwargs):
        signature = self._get_signature(request)
        # request body are bytes, need decode
        json_payload = parse_qs(request.body.decode('utf-8'))['payload'][0]
        try:
            public_key = self._get_travis_public_key()
        except requests.Timeout:
            logger.error({"message":
                "Timed out when attempting to retrieve Travis CI public key"})
            return HttpResponseBadRequest({'status': 'failed'})
        except requests.RequestException as e:
            logger.error({"message":
                "Failed to retrieve Travis CI public key", 'error': e.message})
            return HttpResponseBadRequest({'status': 'failed'})
        try:
            self.check_authorized(signature, public_key, json_payload)
        except SignatureError:
            # Log the failure somewhere
            return HttpResponseBadRequest({'status': 'unauthorized'})
        json_data = json.loads(json_payload)
        # Custom actions
        branch = json_data["branch"]
        error = json_data['status']  # 0 means pass, 1 means fail
        commit = json_data['commit']
        repository_id = json_data['repository']['id']
        if not error:
            if repository_id == 16709902:
                logger.info(
                    f"Auto update to new commit {commit} on branch {branch}")
                subprocess.Popen("bash ~/deploy.sh", shell=True)
            else:
                logger.info(f"Suspicious webhook: {json_data}")
        else:
            logger.info(f"Failed commit {commit} on branch {branch}")
        return JsonResponse({'status': 'received'})

    def check_authorized(self, signature, public_key, payload):
        """
        Convert the PEM encoded public key to a format palatable for pyOpenSSL,
        then verify the signature
        """
        pkey_public_key = load_publickey(FILETYPE_PEM, public_key)
        certificate = X509()
        certificate.set_pubkey(pkey_public_key)
        verify(certificate, signature, payload, str('sha1'))

    def _get_signature(self, request):
        """
        Extract the raw bytes of the request signature provided by travis
        """
        signature = request.META['HTTP_SIGNATURE']
        return base64.b64decode(signature)

    def _get_travis_public_key(self):
        """
        Returns the PEM encoded public key from the Travis CI /config endpoint
        """
        response = requests.get(self.TRAVIS_CONFIG_URL, timeout=10.0)
        response.raise_for_status()
        return response.json(
            )['config']['notifications']['webhook']['public_key']
