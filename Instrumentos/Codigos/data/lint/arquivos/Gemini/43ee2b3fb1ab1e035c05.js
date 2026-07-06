/**
 * Represents a node that triggers a sub-build process.
 *
 * @extends Node
 */
class SubBuildNode extends Node {

	static get type() {

		return 'SubBuild';

	}

	constructor( node, name, nodeType = null ) {

		super( nodeType );

		/**
		 * The node to be built in the sub-build.
		 *
		 * @type {Node}
		 */
		this.node = node;

		/**
		 * The name of the sub-build.
		 *
		 * @type {string}
		 */
		this.name = name;

		/**
		 * This flag can be used for type testing.
		 *
		 * @type {boolean}
		 * @readonly
		 * @default true
		 */
		this.isSubBuildNode = true;

	}

	generateNodeType( builder ) {

		if ( this.nodeType !== null ) return this.nodeType;

		builder.addSubBuild( this.name );

		const nodeType = this.node.getNodeType( builder );

		builder.removeSubBuild();

		return nodeType;

	}

	build( builder, ...params ) {

		builder.addSubBuild( this.name );

		const data = this.node.build( builder, ...params );

		builder.removeSubBuild();

		return data;

	}

}
