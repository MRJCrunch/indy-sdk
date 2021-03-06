package org.hyperledger.indy.sdk.agent;

import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

import org.hyperledger.indy.sdk.IndyException;
import org.hyperledger.indy.sdk.IndyJava;
import org.hyperledger.indy.sdk.LibIndy;
import org.hyperledger.indy.sdk.pool.Pool;
import org.hyperledger.indy.sdk.wallet.Wallet;

import com.sun.jna.Callback;

/**
 * agent.rs API
 */
public class Agent extends IndyJava.API {

	private static Map<Integer, Agent.Connection> connections = new ConcurrentHashMap<Integer, Agent.Connection>();
	private static Map<Integer, Agent.Listener> listeners = new ConcurrentHashMap<Integer, Agent.Listener>();

	private Agent() {

	}

	/*
	 * OBSERVERS
	 */

	private static Map<Integer, AgentObservers.MessageObserver> messageObserver = new ConcurrentHashMap<Integer, AgentObservers.MessageObserver>();
	private static Map<Integer, AgentObservers.ConnectionObserver> connectionObservers = new ConcurrentHashMap<Integer, AgentObservers.ConnectionObserver>();

	private static void addMessageObserver(int commandHandle, AgentObservers.MessageObserver messageObserver) {

		assert(! Agent.messageObserver.containsKey(commandHandle));
		Agent.messageObserver.put(commandHandle, messageObserver);

	}

	private static AgentObservers.MessageObserver removeMessageObserver(int xcommand_handle) {

		AgentObservers.MessageObserver future = messageObserver.remove(xcommand_handle);
		assert(future != null);

		return future;
	}

	private static void addConnectionObserver(int commandHandle, AgentObservers.ConnectionObserver connectionObserver) {

		assert(! connectionObservers.containsKey(commandHandle));
		connectionObservers.put(commandHandle, connectionObserver);

	}

	private static AgentObservers.ConnectionObserver removeConnectionObserver(int xcommand_handle) {

		AgentObservers.ConnectionObserver future = connectionObservers.remove(xcommand_handle);
		assert(future != null);

		return future;
	}

	/*
	 * STATIC CALLBACKS
	 */

	private static Callback agentConnectConnectionCb = new Callback() {

		@SuppressWarnings("unused")
		public void callback(int xcommand_handle, int err, int connection_handle) throws IndyException {

			CompletableFuture<Connection> future = (CompletableFuture<Connection>) removeFuture(xcommand_handle);
			if (! checkCallback(future, err)) return;

			assert(! connections.containsKey(connection_handle));
			Agent.Connection connection = new Agent.Connection(connection_handle);
			connections.put(connection_handle, connection);

			connection.messageObserver = removeMessageObserver(xcommand_handle);

			future.complete(connection);
		}
	};

	private static Callback agentConnectMessageCb = new Callback() {

		@SuppressWarnings("unused")
		public void callback(int xconnection_handle, int err, String message) throws IndyException {

			checkCallback(err);

			Agent.Connection connection = connections.get(xconnection_handle);
			if (connection == null) return;

			AgentObservers.MessageObserver messageObserver = connection.messageObserver;
			messageObserver.onMessage(connection, message);
		}
	};

	private static Callback agentListenListenerCb = new Callback() {

		@SuppressWarnings("unused")
		public void callback(int xcommand_handle, int err, int listener_handle) throws IndyException {

			CompletableFuture<Listener> future = (CompletableFuture<Listener>) removeFuture(xcommand_handle);
			if (! checkCallback(future, err)) return;

			assert(! listeners.containsKey(listener_handle));
			Agent.Listener listener = new Agent.Listener(listener_handle);
			listeners.put(listener_handle, listener);

			listener.connectionObserver = removeConnectionObserver(xcommand_handle);

			future.complete(listener);
		}
	};

	private static Callback agentListenConnectionCb = new Callback() {

		@SuppressWarnings("unused")
		public void callback(int xlistener_handle, int err, int connection_handle, String sender_did, String receiver_did) throws IndyException {

			checkCallback(err);

			Agent.Listener listener = listeners.get(xlistener_handle);
			if (listener == null) return;

			assert(! connections.containsKey(connection_handle));
			Agent.Connection connection = new Agent.Connection(connection_handle);
			connections.put(connection_handle, connection);

			AgentObservers.ConnectionObserver connectionObserver = listener.connectionObserver;
			connection.messageObserver = connectionObserver.onConnection(listener, connection, sender_did, receiver_did);
		}
	};

	private static Callback agentListenMessageCb = new Callback() {

		@SuppressWarnings("unused")
		public void callback(int xconnection_handle, int err, String message) throws IndyException {

			checkCallback(err);

			Agent.Connection connection = connections.get(xconnection_handle);
			if (connection == null) return;

			AgentObservers.MessageObserver messageObserver = connection.messageObserver;
			messageObserver.onMessage(connection, message);
		}
	};

	private static Callback agentAddIdentityCb = new Callback() {

		@SuppressWarnings({"unused", "unchecked"})
		public void callback(int xcommand_handle, int err, int listener_handle) {

			CompletableFuture<Void> future = (CompletableFuture<Void>) removeFuture(xcommand_handle);
			if (! checkCallback(future, err)) return;

			future.complete(null);
		}
	};

	private static Callback agentRemoveIdentityCb = new Callback() {

		@SuppressWarnings({"unused", "unchecked"})
		public void callback(int xcommand_handle, int err, int listener_handle) {

			CompletableFuture<Void> future = (CompletableFuture<Void>) removeFuture(xcommand_handle);
			if (! checkCallback(future, err)) return;

			future.complete(null);
		}
	};

	private static Callback agentSendCb = new Callback() {

		@SuppressWarnings({"unused", "unchecked"})
		public void callback(int xcommand_handle, int err) {

			CompletableFuture<Void> future = (CompletableFuture<Void>) removeFuture(xcommand_handle);
			if (! checkCallback(future, err)) return;

			future.complete(null);
		}
	};

	private static Callback agentCloseConnectionCb = new Callback() {

		@SuppressWarnings({"unused", "unchecked"})
		public void callback(int xcommand_handle, int err) {

			CompletableFuture<Void> future = (CompletableFuture<Void>) removeFuture(xcommand_handle);
			if (! checkCallback(future, err)) return;

			future.complete(null);
		}
	};

	private static Callback agentCloseListenerCb = new Callback() {

		@SuppressWarnings({"unused", "unchecked"})
		public void callback(int xcommand_handle, int err) {

			CompletableFuture<Void> future = (CompletableFuture<Void>) removeFuture(xcommand_handle);
			if (! checkCallback(future, err)) return;

			future.complete(null);
		}
	};

	/*
	 * STATIC METHODS
	 */

	public static CompletableFuture<Connection> agentConnect(
			Pool pool,
			Wallet wallet,
			String senderDid,
			String receiverDid,
			AgentObservers.MessageObserver messageObserver) throws IndyException {

		CompletableFuture<Connection> future = new CompletableFuture<>();
		int commandHandle = addFuture(future);
		addMessageObserver(commandHandle, messageObserver);

		int poolHandle = pool.getPoolHandle();
		int walletHandle = wallet.getWalletHandle();

		int result = LibIndy.api.indy_agent_connect(
				commandHandle,
				poolHandle,
				walletHandle,
				senderDid,
				receiverDid,
				agentConnectConnectionCb,
				agentConnectMessageCb);

		checkResult(result);

		return future;
	}

	public static CompletableFuture<Listener> agentListen(
			String endpoint,
			AgentObservers.ConnectionObserver connectionObserver) throws IndyException {

		CompletableFuture<Listener> future = new CompletableFuture<>();
		int commandHandle = addFuture(future);
		addConnectionObserver(commandHandle, connectionObserver);

		int result = LibIndy.api.indy_agent_listen(
				commandHandle,
				endpoint,
				agentListenListenerCb,
				agentListenConnectionCb,
				agentListenMessageCb);

		checkResult(result);

		return future;
	}

	public static CompletableFuture<Void> agentAddIdentity(
			Agent.Listener listener,
			Pool pool,
			Wallet wallet,
			String did) throws IndyException {

		CompletableFuture<Void> future = new CompletableFuture<Void>();
		int commandHandle = addFuture(future);

		int listenerHandle = listener.getListenerHandle();
		int poolHandle = pool.getPoolHandle();
		int walletHandle = wallet.getWalletHandle();

		int result = LibIndy.api.indy_agent_add_identity(
				commandHandle,
				listenerHandle,
				poolHandle,
				walletHandle,
				did,
				agentAddIdentityCb);

		checkResult(result);

		return future;
	}

	public static CompletableFuture<Void> agentRemoveIdentity(
			Agent.Listener listener,
			Wallet wallet,
			String did) throws IndyException {

		CompletableFuture<Void> future = new CompletableFuture<Void>();
		int commandHandle = addFuture(future);

		int listenerHandle = listener.getListenerHandle();
		int walletHandle = wallet.getWalletHandle();

		int result = LibIndy.api.indy_agent_remove_identity(
				commandHandle,
				listenerHandle,
				walletHandle,
				did,
				agentRemoveIdentityCb);

		checkResult(result);

		return future;
	}

	public static CompletableFuture<Void> agentSend(
			Agent.Connection connection,
			String message) throws IndyException {

		CompletableFuture<Void> future = new CompletableFuture<Void>();
		int commandHandle = addFuture(future);

		int connectionHandle = connection.getConnectionHandle();

		int result = LibIndy.api.indy_agent_send(
				commandHandle,
				connectionHandle,
				message,
				agentSendCb);

		checkResult(result);

		return future;
	}

	public static CompletableFuture<Void> agentCloseConnection(
			Agent.Connection connection) throws IndyException {

		CompletableFuture<Void> future = new CompletableFuture<Void>();
		int commandHandle = addFuture(future);

		int connectionHandle = connection.getConnectionHandle();

		connections.remove(connectionHandle);

		int result = LibIndy.api.indy_agent_close_connection(
				commandHandle,
				connectionHandle,
				agentCloseConnectionCb);

		checkResult(result);

		return future;
	}

	public static CompletableFuture<Void> agentCloseListener(
			Agent.Listener listener) throws IndyException {

		CompletableFuture<Void> future = new CompletableFuture<Void>();
		int commandHandle = addFuture(future);

		int listenerHandle = listener.getListenerHandle();

		listeners.remove(listenerHandle);

		int result = LibIndy.api.indy_agent_close_listener(
				commandHandle,
				listenerHandle,
				agentCloseListenerCb);

		checkResult(result);

		return future;
	}

	/*
	 * NESTED CLASSES WITH INSTANCE METHODS
	 */

	public static class Listener {

		private final int listenerHandle;
		private AgentObservers.ConnectionObserver connectionObserver;

		private Listener(int listenerHandle) {

			this.listenerHandle = listenerHandle;
		}

		public int getListenerHandle() {

			return this.listenerHandle;
		}

		public CompletableFuture<Void> agentAddIdentity(Pool pool, Wallet wallet, String did) throws IndyException {

			return Agent.agentAddIdentity(this, pool, wallet, did);
		}

		public CompletableFuture<Void> agentRemoveIdentity(Wallet wallet, String did) throws IndyException {

			return Agent.agentRemoveIdentity(this, wallet, did);
		}

		public CompletableFuture<Void> agentCloseListener() throws IndyException {

			return Agent.agentCloseListener(this);
		}
	}

	public static class Connection {

		private final int connectionHandle;
		private AgentObservers.MessageObserver messageObserver;

		private Connection(int connectionHandle) {

			this.connectionHandle = connectionHandle;
		}

		public int getConnectionHandle() {

			return this.connectionHandle;
		}

		public CompletableFuture<Void> agentSend(String message) throws IndyException {

			return Agent.agentSend(this, message);
		}

		public CompletableFuture<Void> agentCloseConnection() throws IndyException {

			return Agent.agentCloseConnection(this);
		}
	}
}
