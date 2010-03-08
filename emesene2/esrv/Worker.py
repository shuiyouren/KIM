# -*- coding: utf-8 -*-
import sys
import time
import Queue
import random
import hashlib
import os
from socket import *

import e3

import eclient

import logging
log = logging.getLogger('esvr.Worker')

class Worker(e3.Worker):
    '''eclient implementation.'''
    NOTIFICATION_DELAY = 3

    def __init__(self, app_name, session, proxy, use_http=False):
        '''class constructor'''
        e3.Worker.__init__(self, app_name, session)
        self.session = session
        self.conversations = {}
        self.rconversations = {}
        self.contacts = {}
        self.flag = 0
        self.eclient = None

        self.port = 1864

        self.debug = 3
        self.frequency = 0.1

        self.host = session.DEFAULT_HOST
        self.hport = session.DEFAULT_PORT

        #print self.session.config_dir.base_dir
        #self.caches = e3.cache.CacheManager(self.session.config_dir.base_dir)

    def run(self):
			'''main method, block waiting for data, process it, and send data back
			'''
			data = None

			while True:
				try:
					action = self.session.actions.get(True, 0.1)

					if action.id_ == e3.Action.ACTION_QUIT:
							log.debug('closing thread')
							self.session.logger.quit()
							break

					self._process_action(action)
				except Queue.Empty:
					pass


    def _fill_contact_list(self, doc):
		"""
		method to fill the contact list with something
		"""

		contactsDom = doc.getElementsByTagName('contact')

		self._add_group('friends')

		self.myIP = doc.getElementsByTagName('clientip')[0].firstChild.nodeValue
		#print "eee"+myIP

		for contact in contactsDom:
			#print "extrae"
			contactIP = contact.getElementsByTagName('ip')[0].firstChild.nodeValue
			contactNick = contact.getElementsByTagName('nick')[0].firstChild.nodeValue
			contactSubnick = contact.getElementsByTagName('subnick')[0].firstChild.nodeValue
			contactUser = contact.getElementsByTagName('user')[0].firstChild.nodeValue
			contactStatus = contact.getElementsByTagName('status')[0].firstChild.nodeValue
			contactPort = 1864

			user = {}
			user['ip'] = contactIP

			self.contacts[contactUser] = user


			if self.debug>0: print contactNick+" offline on "+self.contacts[contactUser]['ip']
			contactStatus=e3.status.OFFLINE

			#self._add_contact(contactNick, contactSubnick, contactStatus, '', False)
			self._add_contact(contactUser, contactNick, contactSubnick,  contactStatus, '', False)
			self._add_contact_to_group(contactUser, 'friends')


    def _add_contact(self, mail, nick, subnick, status_, alias, blocked):
        """
        method to add a contact to the contact list
        """
        #self.session.contacts.contacts[mail] = e3.Contact(mail, mail,
        #    nick, '...', status_, alias, blocked)
        self.session.contacts.contacts[mail] = e3.Contact(mail, mail,
            nick, subnick, status_, alias, blocked)

    def _add_group(self, name):
        """
        method to add a group to the contact list
        """
        self.session.groups[name] = e3.Group(name, name)

    def _add_contact_to_group(self, account, group):
        """
        method to add a contact to a group
        """
        self.session.groups[group].contacts.append(account)
        self.session.contacts.contacts[account].groups.append(group)

    def _eclient_login_info (self, info ):
        self.session.add_event(e3.Event.EVENT_LOGIN_INFO, info)

    def _eclient_refresh_contact (self, contact_info ):

        if self.debug>1: print "[worker] Refresh contact: "+contact_info['user']

        status = contact_info['status']
        user = contact_info['user']
        subnick = contact_info['subnick']
        nick = contact_info['nick']
        avatar = contact_info['avatar']

        currentStamp = self.eclient.getStamp ()

        dif = currentStamp - int (contact_info['stamp'])

        if self.debug>1: print "CurrentStamp: "+str(currentStamp)+", ContactStamp: "+str(contact_info['stamp'])+" Dif: "+str ( dif )

        if dif > 30:
            status = e3.status.OFFLINE

        if ( int (contact_info['stamp']) == 0 ):
            status = e3.status.OFFLINE

        self.contacts[ user ] = contact_info

        if status == eclient.status.OFFLINE:
            change_type = 'offline'
        else:
            change_type = 'online'

        if self.debug>1: print "Status: "+str(status)

        if status == eclient.status.ONLINE:
            e3status = e3.status.ONLINE
        elif status == eclient.status.BUSY:
            e3status = e3.status.BUSY
        elif status == eclient.status.AWAY:
            e3status = e3.status.AWAY
        elif status == eclient.status.IDLE:
            e3status = e3.status.IDLE
        else:
            e3status = e3.status.OFFLINE

        #old_status = e3.status.OFFLINE
        #status = e3.status.ONLINE

        contactOb = self.session.contacts.contacts.get( user , None)

        avatars = self.caches.get_avatar_cache( user )
        avatar_path = os.path.join(avatars.path, avatar)

        old_e3status = contactOb.status
        old_subnick = contactOb.message
        old_nick = contactOb.nick
        old_avatar = contactOb.picture
        old_media = 'Old'
        media = 'New'

        contactOb.status = e3status
        contactOb.message = subnick
        contactOb.nick = nick
        contactOb.media = media

        if self.debug>1: print "[worker] Offline="+str(e3.status.OFFLINE)+", Changetipe="+change_type+", Old status: "+str(old_e3status)+", New: "+str(e3status)

        log_account =  e3.Logger.Account(contactOb.attrs.get('CID', None), None,
            contactOb.account, contactOb.status, contactOb.nick, contactOb.message,
            contactOb.picture)

        #str(old_status)
        if old_e3status != e3status:
            if self.debug>0: print "[worker] Changing Status"

            start_time = 1

            do_notify = (start_time + Worker.NOTIFICATION_DELAY) < time.time()

            self.session.add_event(e3.Event.EVENT_CONTACT_ATTR_CHANGED, user, change_type, old_e3status, do_notify)
            self.session.logger.log('status change', e3status, str(e3status),
                log_account)

        if old_subnick != subnick:
            if self.debug>0: print "[worker] Changing Subnick: "+subnick
            self.session.add_event(e3.Event.EVENT_CONTACT_ATTR_CHANGED, user,
                'message', old_subnick)
            self.session.logger.log('message change', e3status,
                subnick, log_account)

        if old_nick != nick:
            if self.debug>0: print "[worker] Changing Nick: "+nick
            self.session.add_event(e3.Event.EVENT_CONTACT_ATTR_CHANGED, user,
                'nick', old_nick)
            self.session.logger.log('nick change', e3status, nick,
                log_account)

        if old_media != media:
            self.session.add_event(e3.Event.EVENT_CONTACT_ATTR_CHANGED, user,
                'media', old_media)

        #print "OLD: "+str(old_avatar)
        #print "NEW: "+str(avatar_path)

        if old_avatar != avatar_path:
            if avatar != '-':
                print "AVATAR : "+str(avatar_path)
                
                ihave = 0

                if os.path.exists(avatar_path):
                    print "EXIST"
                    ihave = 1
                else:
                    print "DOWNLOADDING"
                    avatar_raw = self.eclient.retrieveAvatar ( user )

                    #avatar_caches = e3.cache.AvatarCache(self.session.config_dir.base_dir, self.session.account.account)

                    #if ( avatar_raw != None ): time_, ava_md5 = avatar_caches.insert_raw( avatar_raw )

                    if ( avatar_raw != None ):
                        ava_path = os.path.join( self.caches.get_avatar_cache( user ).path , avatar+".tmp")
                        handle = file(ava_path, 'w')
                        handle.write(avatar_raw.read())
                        handle.close()

                        avatar_caches = e3.cache.AvatarCache(self.session.config_dir.base_dir, user)
                        time_, ava_md5 = avatar_caches.insert( ava_path )
                        ihave = 1

                if ihave == 1:
                    print "SETTING"
                    contactOb.picture = avatar_path
                    self.session.add_event( e3.Event.EVENT_PICTURE_CHANGE_SUCCEED, user, avatar_path )

    # action handlers
    def _handle_action_add_contact(self, account):
        '''handle Action.ACTION_ADD_CONTACT
        '''
        print "Add Contact: "+ str ( account )
        self.eclient.addContact ( account )
        self.session.add_event(e3.Event.EVENT_CONTACT_ADD_SUCCEED,
            account)

    def _handle_action_add_group(self, name):
        '''handle Action.ACTION_ADD_GROUP
        '''
        print "Add Group: "+ str ( account )
        self.session.add_event(e3.Event.EVENT_GROUP_ADD_SUCCEED,
            name)

    def _handle_action_add_to_group(self, account, gid):
        '''handle Action.ACTION_ADD_TO_GROUP
        '''
        self.session.add_event(e3.Event.EVENT_GROUP_ADD_CONTACT_SUCCEED,
            gid, account)

    def _handle_action_block_contact(self, account):
        '''handle Action.ACTION_BLOCK_CONTACT
        '''
        print "Block Contact: "+ str ( account )
        self.session.add_event(e3.Event.EVENT_CONTACT_BLOCK_SUCCEED, account)

    def _handle_action_unblock_contact(self, account):
        '''handle Action.ACTION_UNBLOCK_CONTACT
        '''
        print "Unblock Contact: "+ str ( account )
        self.session.add_event(e3.Event.EVENT_CONTACT_UNBLOCK_SUCCEED,
            account)

    def _handle_action_change_status(self, status_):
        '''handle Action.ACTION_CHANGE_STATUS
        '''
        if self.debug>0: print "New Status: "+str(status_)
        self.session.account.status = status_
        self.session.contacts.me.status = status_
        self.session.add_event(e3.Event.EVENT_STATUS_CHANGE_SUCCEED, status_)

        if status_ == e3.status.ONLINE:
            estatus = eclient.status.ONLINE
        if status_ == e3.status.BUSY:
            estatus = eclient.status.BUSY
        if status_ == e3.status.AWAY:
            estatus = eclient.status.AWAY
        if status_ == e3.status.IDLE:
            estatus = eclient.status.IDLE
        if status_ == e3.status.OFFLINE:
            estatus = eclient.status.OFFLINE

        self.eclient.status_ = estatus

    def _handle_action_login(self, account, password, status_, host, port):
        '''handle Action.ACTION_LOGIN
        '''
        self.session.add_event(e3.Event.EVENT_LOGIN_STARTED)


        self.eclient = eclient.client ( account, password, host, port )

        self.eclient.debug = self.debug
        self.eclient.frequency = self.frequency
        self.eclient.debug = self.debug

        if status_ == e3.status.ONLINE:
            estatus = eclient.status.ONLINE
        if status_ == e3.status.BUSY:
            estatus = eclient.status.BUSY
        if status_ == e3.status.AWAY:
            estatus = eclient.status.AWAY
        if status_ == e3.status.IDLE:
            estatus = eclient.status.IDLE
        if status_ == e3.status.OFFLINE:
            estatus = eclient.status.OFFLINE

        if self.debug>0:  print "[login] LOGIN"

        '''
        self.eclient.set_onMessage ( self._eclient_on_message_received )
        self.eclient.set_onContactUpdate ( self._eclient_refresh_contact )
        '''

        if self.eclient.login( estatus, self._eclient_login_info ):
            '''
            nick =self.eclient.getNick()
            subnick = self.eclient.getSubnick()
            avatar = self.eclient.getAvatar()
            self.session.add_event(e3.Event.EVENT_LOGIN_SUCCEED)
            
            self._add_group('friends')
            contactStatus=e3.status.OFFLINE

            contactList = self.eclient.getContactList ()

            if self.debug>0:  print "[login] CONTACTS"

            for contact in contactList:

                self._add_contact( contact , contactList[ contact ]['nick'], contactList[ contact ]['subnick'],  contactStatus, '', False)
                self._add_contact_to_group( contact, 'friends' )


            if self.debug>0:  print "[login] OPENPORT"

            self.eclient.open_listenport ( self.port, 20, 10 )

            self.session.account.status = status_
            self.session.contacts.me.status = status_
            self.session.add_event(e3.Event.EVENT_STATUS_CHANGE_SUCCEED, status_)

            self.session.add_event(e3.Event.EVENT_NICK_CHANGE_SUCCEED, nick)
            self.session.contacts.me.nick = nick
            self.session.add_event(e3.Event.EVENT_MESSAGE_CHANGE_SUCCEED, subnick)
            self.session.contacts.me.message = subnick

            if self.debug>0:  print "[login] OK"
            self.contacts = self.eclient.getContactList()
            '''
            self.session.add_event(e3.Event.EVENT_CONTACT_LIST_READY)
            '''
            self.eclient.start_refreshing ()
            self.eclient.start_http ()

            print account
            avatars = self.caches.get_avatar_cache( account )
            avatar_path = os.path.join(avatars.path, avatar)
            self.eclient.avatar_path = avatar_path

            print avatar_path
            self.session.contacts.me.picture = avatar_path
            self.session.add_event( e3.Event.EVENT_PICTURE_CHANGE_SUCCEED, account, avatar_path )
            '''
        else:
            if self.eclient.getError() == eclient.error.CONN:
                self.session.add_event(e3.Event.EVENT_DISCONNECTED, 'Server down' )
            elif self.eclient.getError() == eclient.error.AUTH:
                self.session.add_event(e3.Event.EVENT_LOGIN_FAILED, )





    def _handle_action_logout(self):
        '''handle Action.ACTION_LOGOUT
        '''
        self.eclient.logout

    def _handle_action_move_to_group(self, account, src_gid, dest_gid):
        '''handle Action.ACTION_MOVE_TO_GROUP
        '''
        self.session.add_event(e3.Event.EVENT_CONTACT_MOVE_SUCCEED,
            account, src_gid, dest_gid)

    def _handle_action_remove_contact(self, account):
        '''handle Action.ACTION_REMOVE_CONTACT
        '''
        print "Remove contact: "+ str ( account )
        self.session.add_event(e3.Event.EVENT_CONTACT_REMOVE_SUCCEED, account)

    def _handle_action_reject_contact(self, account):
        '''handle Action.ACTION_REJECT_CONTACT
        '''
        self.session.add_event(e3.Event.EVENT_CONTACT_REJECT_SUCCEED, account)

    def _handle_action_remove_from_group(self, account, gid):
        '''handle Action.ACTION_REMOVE_FROM_GROUP
        '''
        self.session.add_event(e3.Event.EVENT_GROUP_REMOVE_CONTACT_SUCCEED,
            gid, account)

    def _handle_action_remove_group(self, gid):
        '''handle Action.ACTION_REMOVE_GROUP
        '''
        self.session.add_event(e3.Event.EVENT_GROUP_REMOVE_SUCCEED, gid)

    def _handle_action_rename_group(self, gid, name):
        '''handle Action.ACTION_RENAME_GROUP
        '''
        self.session.add_event(e3.Event.EVENT_GROUP_RENAME_SUCCEED,
            gid, name)

    def _handle_action_set_contact_alias(self, account, alias):
        '''handle Action.ACTION_SET_CONTACT_ALIAS
        '''
        self.session.add_event(e3.Event.EVENT_CONTACT_ALIAS_SUCCEED, account)

    def _handle_action_set_message(self, message):
        '''handle Action.ACTION_SET_MESSAGE
        '''
        if self.eclient.setSubnick ( message ):
            self.session.add_event(e3.Event.EVENT_MESSAGE_CHANGE_SUCCEED, message)

    def _handle_action_set_nick(self, nick):
        '''handle Action.ACTION_SET_NICK
        '''
        if self.eclient.setNick ( nick ):
            self.session.add_event(e3.Event.EVENT_NICK_CHANGE_SUCCEED, nick)

    def _handle_action_set_picture(self, picture_name):
        '''handle Action.ACTION_SET_PICTURE
        '''

        avatar_caches = e3.cache.AvatarCache(self.session.config_dir.base_dir, self.session.account.account)

        time, ava_md5 = avatar_caches.insert( picture_name )

        self.eclient.setAvatar( ava_md5 )

        self.eclient.avatar_path = os.path.join( self.caches.get_avatar_cache( self.session.account.account ).path , ava_md5)
        self.session.contacts.me.picture = picture_name
        self.session.add_event(e3.Event.EVENT_PICTURE_CHANGE_SUCCEED, self.session.account.account, picture_name)

    def _handle_action_set_preferences(self, preferences):
        '''handle Action.ACTION_SET_PREFERENCES
        '''
        pass

    def _handle_action_new_conversation(self, account, cid):
        '''handle Action.ACTION_NEW_CONVERSATION
        '''
        self.conversations[account] = cid
        self.rconversations[cid] = [account]
        if self.debug>0: print ( "New conversation: SID: "+ str ( cid ) )
        pass

    def _handle_action_close_conversation(self, cid):
        '''handle Action.ACTION_CLOSE_CONVERSATION
        '''
        pass

    def _handle_action_send_message(self, cid, message):
            if self.debug>1: print "Sending message"
            '''handle Action.ACTION_SEND_MESSAGE
            cid is the conversation id, message is a Message object
            '''

            if self.debug>1: print ( "Old conversation: SID: "+ str ( cid ) )

            recipients = self.rconversations.get(cid, ())[0]
            #if len ( recipients )>0: recipients = recipients[0]
            body = message.body

            self.eclient.sendMessage ( body, recipients )

            #account = random.choice(self.session.contacts.contacts.keys())

            #recipients = self.rconversations.get(cid, ())
            self.session.add_event(e3.Event.EVENT_CONV_MESSAGE_SEND_SUCCEED, cid, message)


    def _eclient_on_message_received( self, body, sender):
        if sender in self.conversations:
            cid = self.conversations[sender]
        else:
            cid = time.time()
            self.conversations[sender] = cid
            self.rconversations[cid] = [sender]
            self.session.add_event(e3.Event.EVENT_CONV_FIRST_ACTION, cid, [sender])

        type_ = e3.Message.TYPE_MESSAGE
        msgobj = e3.Message(type_, body, sender)

        self.session.add_event(e3.Event.EVENT_CONV_MESSAGE, cid, sender, msgobj)

    # p2p handlers

    def _handle_action_p2p_invite(self, cid, pid, dest, type_, identifier):
        '''handle Action.ACTION_P2P_INVITE,
         cid is the conversation id
         pid is the p2p session id, both are numbers that identify the
            conversation and the session respectively, time.time() is
            recommended to be used.
         dest is the destination account
         type_ is one of the e3.Transfer.TYPE_* constants
         identifier is the data that is needed to be sent for the invitation
        '''
        pass

    def _handle_action_p2p_accept(self, pid):
        '''handle Action.ACTION_P2P_ACCEPT'''
        pass

    def _handle_action_p2p_cancel(self, pid):
        '''handle Action.ACTION_P2P_CANCEL'''
        pass
