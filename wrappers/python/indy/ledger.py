from .libindy import do_call, create_cb

from typing import Optional
from ctypes import *

import logging


async def sign_and_submit_request(pool_handle: int,
                                  wallet_handle: int,
                                  submitter_did: str,
                                  request_json: str) -> str:
    """
    Signs and submits request message to validator pool.

    Adds submitter information to passed request json, signs it with submitter
    sign key (see wallet_sign), and sends signed request message
    to validator pool (see write_request).

    :param pool_handle: pool handle (created by open_pool_ledger).
    :param wallet_handle: wallet handle (created by open_wallet).
    :param submitter_did: Id of Identity stored in secured Wallet.
    :param request_json: Request data json.
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("sign_and_submit_request: >>> pool_handle: %s, wallet_handle: %s, submitter_did: %s, request_json: %s",
                 pool_handle,
                 wallet_handle,
                 submitter_did,
                 request_json)

    if not hasattr(sign_and_submit_request, "cb"):
        logger.debug("sign_and_submit_request: Creating callback")
        sign_and_submit_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_pool_handle = c_int32(pool_handle)
    c_wallet_handle = c_int32(wallet_handle)
    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_request_json = c_char_p(request_json.encode('utf-8'))

    request_result = await do_call('indy_sign_and_submit_request',
                                   c_pool_handle,
                                   c_wallet_handle,
                                   c_submitter_did,
                                   c_request_json,
                                   sign_and_submit_request.cb)

    res = request_result.decode()
    logger.debug("sign_and_submit_request: <<< res: %s", res)
    return res


async def submit_request(pool_handle: int,
                         request_json: str) -> str:
    """
    Publishes request message to validator pool (no signing, unlike sign_and_submit_request).
    The request is sent to the validator pool as is. It's assumed that it's already prepared.

    :param pool_handle: pool handle (created by open_pool_ledger).
    :param request_json: Request data json.
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("submit_request: >>> pool_handle: %s, request_json: %s",
                 pool_handle,
                 request_json)

    if not hasattr(submit_request, "cb"):
        logger.debug("submit_request: Creating callback")
        submit_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_pool_handle = c_int32(pool_handle)
    c_request_json = c_char_p(request_json.encode('utf-8'))

    request_result = await do_call('indy_submit_request',
                                   c_pool_handle,
                                   c_request_json,
                                   submit_request.cb)

    res = request_result.decode()
    logger.debug("submit_request: <<< res: %s", res)
    return res


async def build_get_ddo_request(submitter_did: str,
                                target_did: str) -> str:
    """
    Builds a request to get a DDO.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param target_did: Id of Identity stored in secured Wallet.
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_get_ddo_request: >>> submitter_did: %s, target_did: %s",
                 submitter_did,
                 target_did)

    if not hasattr(build_get_ddo_request, "cb"):
        logger.debug("build_get_ddo_request: Creating callback")
        build_get_ddo_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_target_did = c_char_p(target_did.encode('utf-8'))

    request_json = await do_call('indy_build_get_ddo_request',
                                 c_submitter_did,
                                 c_target_did,
                                 build_get_ddo_request.cb)

    res = request_json.decode()
    logger.debug("build_get_ddo_request: <<< res: %s", res)
    return res


async def build_nym_request(submitter_did: str,
                            target_did: str,
                            ver_key: Optional[str],
                            alias: Optional[str],
                            role: Optional[str]) -> str:
    """
    Builds a NYM request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param target_did: Id of Identity stored in secured Wallet.
    :param ver_key: verification key
    :param alias: alias
    :param role: Role of a user NYM record
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_nym_request: >>> submitter_did: %s, target_did: %s, ver_key: %s, alias: %s, role: %s",
                 submitter_did,
                 target_did,
                 ver_key,
                 alias,
                 role)

    if not hasattr(build_nym_request, "cb"):
        logger.debug("build_nym_request: Creating callback")
        build_nym_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_target_did = c_char_p(target_did.encode('utf-8'))
    c_ver_key = c_char_p(ver_key.encode('utf-8')) if ver_key is not None else None
    c_alias = c_char_p(alias.encode('utf-8')) if alias is not None else None
    c_role = c_char_p(role.encode('utf-8')) if role is not None else None

    request_json = await do_call('indy_build_nym_request',
                                 c_submitter_did,
                                 c_target_did,
                                 c_ver_key,
                                 c_alias,
                                 c_role,
                                 build_nym_request.cb)

    res = request_json.decode()
    logger.debug("build_nym_request: <<< res: %s", res)
    return res


async def build_attrib_request(submitter_did: str,
                               target_did: str,
                               xhash: Optional[str],
                               raw: Optional[str],
                               enc: Optional[str]) -> str:
    """
    Builds an ATTRIB request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param target_did: Id of Identity stored in secured Wallet.
    :param hash: Hash of attribute data
    :param raw: represented as json, where key is attribute name and value is it's value
    :param enc: Encrypted attribute data
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_attrib_request: >>> submitter_did: %s, target_did: %s, hash: %s, raw: %s, enc: %s",
                 submitter_did,
                 target_did,
                 xhash,
                 raw,
                 enc)

    if not hasattr(build_attrib_request, "cb"):
        logger.debug("build_attrib_request: Creating callback")
        build_attrib_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_target_did = c_char_p(target_did.encode('utf-8'))
    c_hash = c_char_p(xhash.encode('utf-8')) if xhash is not None else None
    c_raw = c_char_p(raw.encode('utf-8')) if raw is not None else None
    c_enc = c_char_p(enc.encode('utf-8')) if enc is not None else None

    request_json = await do_call('indy_build_attrib_request',
                                 c_submitter_did,
                                 c_target_did,
                                 c_hash,
                                 c_raw,
                                 c_enc,
                                 build_attrib_request.cb)

    res = request_json.decode()
    logger.debug("build_attrib_request: <<< res: %s", res)
    return res


async def build_get_attrib_request(submitter_did: str,
                                   target_did: str,
                                   data: str) -> str:
    """
    Builds a GET_ATTRIB request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param target_did: Id of Identity stored in secured Wallet.
    :param data: name (attribute name)
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_get_attrib_request: >>> submitter_did: %s, target_did: %s, data: %s",
                 submitter_did,
                 target_did,
                 data)

    if not hasattr(build_get_attrib_request, "cb"):
        logger.debug("build_get_attrib_request: Creating callback")
        build_get_attrib_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_target_did = c_char_p(target_did.encode('utf-8'))
    c_data = c_char_p(data.encode('utf-8'))

    request_json = await do_call('indy_build_get_attrib_request',
                                 c_submitter_did,
                                 c_target_did,
                                 c_data,
                                 build_get_attrib_request.cb)

    res = request_json.decode()
    logger.debug("build_get_attrib_request: <<< res: %s", res)
    return res


async def build_get_nym_request(submitter_did: str,
                                target_did: str) -> str:
    """
    Builds a GET_NYM request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param target_did: Id of Identity stored in secured Wallet.
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_get_nym_request: >>> submitter_did: %s, target_did: %s",
                 submitter_did,
                 target_did)

    if not hasattr(build_get_nym_request, "cb"):
        logger.debug("build_get_nym_request: Creating callback")
        build_get_nym_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_target_did = c_char_p(target_did.encode('utf-8'))

    request_json = await do_call('indy_build_get_nym_request',
                                 c_submitter_did,
                                 c_target_did,
                                 build_get_nym_request.cb)

    res = request_json.decode()
    logger.debug("build_get_nym_request: <<< res: %s", res)
    return res


async def build_schema_request(submitter_did: str,
                               data: str) -> str:
    """
    Builds a SCHEMA request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param data: name, version, type, attr_names (ip, port, keys)
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_schema_request: >>> submitter_did: %s, data: %s",
                 submitter_did,
                 data)

    if not hasattr(build_schema_request, "cb"):
        logger.debug("build_schema_request: Creating callback")
        build_schema_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_data = c_char_p(data.encode('utf-8'))

    request_json = await do_call('indy_build_schema_request',
                                 c_submitter_did,
                                 c_data,
                                 build_schema_request.cb)

    res = request_json.decode()
    logger.debug("build_schema_request: <<< res: %s", res)
    return res


async def build_get_schema_request(submitter_did: str,
                                   dest: str,
                                   data: str) -> str:
    """
    Builds a GET_SCHEMA request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param dest: Id of Identity stored in secured Wallet.
    :param data: name, version
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_get_schema_request: >>> submitter_did: %s, dest: %s, data: %s",
                 submitter_did,
                 dest,
                 data)

    if not hasattr(build_get_schema_request, "cb"):
        logger.debug("build_get_schema_request: Creating callback")
        build_get_schema_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_dest = c_char_p(dest.encode('utf-8'))
    c_data = c_char_p(data.encode('utf-8'))

    request_json = await do_call('indy_build_get_schema_request',
                                 c_submitter_did,
                                 c_dest,
                                 c_data,
                                 build_get_schema_request.cb)

    res = request_json.decode()
    logger.debug("build_get_schema_request: <<< res: %s", res)
    return res


async def build_claim_def_txn(submitter_did: str,
                              xref: int,
                              signature_type: str,
                              data: str) -> str:
    """
    Builds an CLAIM_DEF request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param xref: Seq. number of schema
    :param signature_type: signature type (only CL supported now)
    :param data: components of a key in json: N, R, S, Z
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_get_schema_request: >>> submitter_did: %s, xref: %s, signature_type: %s, data: %s",
                 submitter_did,
                 xref,
                 signature_type,
                 data)

    if not hasattr(build_claim_def_txn, "cb"):
        logger.debug("build_claim_def_txn: Creating callback")
        build_claim_def_txn.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_xref = c_int32(xref)
    c_signature_type = c_char_p(signature_type.encode('utf-8'))
    c_data = c_char_p(data.encode('utf-8'))

    request_result = await do_call('indy_build_claim_def_txn',
                                   c_submitter_did,
                                   c_xref,
                                   c_signature_type,
                                   c_data,
                                   build_claim_def_txn.cb)

    res = request_result.decode()
    logger.debug("build_claim_def_txn: <<< res: %s", res)
    return res


async def build_get_claim_def_txn(submitter_did: str,
                                  xref: int,
                                  signature_type: str,
                                  origin: str) -> str:
    """
    Builds a GET_CLAIM_DEF request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param xref: Seq. number of schema
    :param signature_type: signature type (only CL supported now)
    :param origin: issuer did
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_get_claim_def_txn: >>> submitter_did: %s, xref: %s, signature_type: %s, origin: %s",
                 submitter_did,
                 xref,
                 signature_type,
                 origin)

    if not hasattr(build_get_claim_def_txn, "cb"):
        logger.debug("build_get_claim_def_txn: Creating callback")
        build_get_claim_def_txn.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_xref = c_int32(xref)
    c_signature_type = c_char_p(signature_type.encode('utf-8'))
    c_origin = c_char_p(origin.encode('utf-8'))

    request_json = await do_call('indy_build_get_claim_def_txn',
                                 c_submitter_did,
                                 c_xref,
                                 c_signature_type,
                                 c_origin,
                                 build_get_claim_def_txn.cb)

    res = request_json.decode()
    logger.debug("build_get_claim_def_txn: <<< res: %s", res)
    return res


async def build_node_request(submitter_did: str,
                             target_did: str,
                             data: str) -> str:
    """
    Builds a NODE request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param target_did: Id of Identity stored in secured Wallet.
    :param data: id of a target NYM record
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_node_request: >>> submitter_did: %s, target_did: %s, data: %s",
                 submitter_did,
                 target_did,
                 data)

    if not hasattr(build_node_request, "cb"):
        logger.debug("build_node_request: Creating callback")
        build_node_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_target_did = c_char_p(target_did.encode('utf-8'))
    c_data = c_char_p(data.encode('utf-8'))

    request_json = await do_call('indy_build_node_request',
                                 c_submitter_did,
                                 c_target_did,
                                 c_data,
                                 build_node_request.cb)

    res = request_json.decode()
    logger.debug("build_node_request: <<< res: %s", res)
    return res


async def build_get_txn_request(submitter_did: str,
                                data: int) -> str:
    """
    Builds a GET_TXN request.

    :param submitter_did: Id of Identity stored in secured Wallet.
    :param data: seq_no of transaction in ledger
    :return: Request result as json.
    """

    logger = logging.getLogger(__name__)
    logger.debug("build_get_txn_request: >>> submitter_did: %s, data: %s",
                 submitter_did,
                 data)

    if not hasattr(build_get_txn_request, "cb"):
        logger.debug("build_get_txn_request: Creating callback")
        build_get_txn_request.cb = create_cb(CFUNCTYPE(None, c_int32, c_int32, c_char_p))

    c_submitter_did = c_char_p(submitter_did.encode('utf-8'))
    c_data = c_int32(data)

    request_json = await do_call('indy_build_get_txn_request',
                                 c_submitter_did,
                                 c_data,
                                 build_get_txn_request.cb)

    res = request_json.decode()
    logger.debug("build_get_txn_request: <<< res: %s", res)
    return res
